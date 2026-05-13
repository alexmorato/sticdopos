#!/usr/bin/env python3
"""Convert EPUB files to Markdown.

Usage:
	python epubtomd.py input.epub -o output.md
"""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


DOC_MEDIA_TYPES = {
	"application/xhtml+xml",
	"text/html",
}


def collapse_blank_lines(text: str) -> str:
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = re.sub(r"[ \t]+\n", "\n", text)
	text = re.sub(r"\n{3,}", "\n\n", text)
	return text.strip() + "\n"


class HTMLToMarkdownParser(HTMLParser):
	"""Small HTML to Markdown parser tuned for common EPUB XHTML."""

	def __init__(self) -> None:
		super().__init__(convert_charrefs=True)
		self.parts: list[str] = []
		self.skip_depth = 0
		self.in_pre = False
		self.in_code = False
		self.current_href = ""
		self.list_stack: list[dict[str, int | str]] = []

	def get_markdown(self) -> str:
		return collapse_blank_lines("".join(self.parts))

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		if tag in {"script", "style"}:
			self.skip_depth += 1
			return
		if self.skip_depth:
			return

		attr_map = {k: (v or "") for k, v in attrs}

		if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
			level = int(tag[1])
			self.parts.append(f"\n{'#' * level} ")
		elif tag == "p":
			self.parts.append("\n\n")
		elif tag == "br":
			self.parts.append("  \n")
		elif tag in {"strong", "b"}:
			self.parts.append("**")
		elif tag in {"em", "i"}:
			self.parts.append("*")
		elif tag == "code":
			if self.in_pre:
				return
			self.in_code = True
			self.parts.append("`")
		elif tag == "pre":
			self.in_pre = True
			self.parts.append("\n\n```\n")
		elif tag in {"ul", "ol"}:
			kind = "ordered" if tag == "ol" else "unordered"
			self.list_stack.append({"kind": kind, "index": 1})
			self.parts.append("\n")
		elif tag == "li":
			indent = "  " * max(0, len(self.list_stack) - 1)
			if self.list_stack and self.list_stack[-1]["kind"] == "ordered":
				idx = int(self.list_stack[-1]["index"])
				self.parts.append(f"\n{indent}{idx}. ")
				self.list_stack[-1]["index"] = idx + 1
			else:
				self.parts.append(f"\n{indent}- ")
		elif tag == "blockquote":
			self.parts.append("\n\n> ")
		elif tag == "a":
			self.current_href = attr_map.get("href", "")
			self.parts.append("[")
		elif tag == "img":
			alt = attr_map.get("alt", "")
			src = attr_map.get("src", "")
			self.parts.append(f"![{alt}]({src})")
		elif tag == "hr":
			self.parts.append("\n\n---\n\n")

	def handle_endtag(self, tag: str) -> None:
		if tag in {"script", "style"}:
			self.skip_depth = max(0, self.skip_depth - 1)
			return
		if self.skip_depth:
			return

		if tag in {"strong", "b"}:
			self.parts.append("**")
		elif tag in {"em", "i"}:
			self.parts.append("*")
		elif tag == "code" and self.in_code:
			self.in_code = False
			self.parts.append("`")
		elif tag == "pre":
			self.in_pre = False
			self.parts.append("\n```\n")
		elif tag in {"ul", "ol"} and self.list_stack:
			self.list_stack.pop()
			self.parts.append("\n")
		elif tag == "a":
			href = self.current_href
			self.parts.append(f"]({href})" if href else "]")
			self.current_href = ""

	def handle_data(self, data: str) -> None:
		if self.skip_depth:
			return
		if not data:
			return
		if self.in_pre:
			self.parts.append(data)
			return
		text = html.unescape(data)
		text = re.sub(r"\s+", " ", text)
		self.parts.append(text)


@dataclass
class EpubMetadata:
	title: str = ""
	creator: str = ""
	language: str = ""


def _decode_xml(raw: bytes) -> str:
	for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
		try:
			return raw.decode(enc)
		except UnicodeDecodeError:
			continue
	return raw.decode("utf-8", errors="replace")


def find_opf_path(zf: zipfile.ZipFile) -> str:
	container_xml = zf.read("META-INF/container.xml")
	root = ET.fromstring(container_xml)
	ns = {
		"c": "urn:oasis:names:tc:opendocument:xmlns:container",
	}
	node = root.find(".//c:rootfile", ns)
	if node is None:
		raise ValueError("No rootfile entry found in META-INF/container.xml")
	opf_path = node.attrib.get("full-path", "").strip()
	if not opf_path:
		raise ValueError("Rootfile full-path is empty")
	return opf_path


def parse_metadata(opf_root: ET.Element, ns: dict[str, str]) -> EpubMetadata:
	md = EpubMetadata()
	title_node = opf_root.find(".//dc:title", ns)
	creator_node = opf_root.find(".//dc:creator", ns)
	lang_node = opf_root.find(".//dc:language", ns)
	md.title = (title_node.text or "").strip() if title_node is not None else ""
	md.creator = (creator_node.text or "").strip() if creator_node is not None else ""
	md.language = (lang_node.text or "").strip() if lang_node is not None else ""
	return md


def read_epub_documents(epub_path: Path) -> tuple[EpubMetadata, list[str]]:
	with zipfile.ZipFile(epub_path, "r") as zf:
		opf_path = find_opf_path(zf)
		opf_dir = posixpath.dirname(opf_path)
		opf_root = ET.fromstring(zf.read(opf_path))

		ns = {
			"opf": "http://www.idpf.org/2007/opf",
			"dc": "http://purl.org/dc/elements/1.1/",
		}

		metadata = parse_metadata(opf_root, ns)

		manifest: dict[str, tuple[str, str]] = {}
		for item in opf_root.findall(".//opf:manifest/opf:item", ns):
			item_id = item.attrib.get("id", "")
			href = item.attrib.get("href", "")
			media = item.attrib.get("media-type", "")
			if item_id and href:
				manifest[item_id] = (href, media)

		doc_paths: list[str] = []
		for itemref in opf_root.findall(".//opf:spine/opf:itemref", ns):
			idref = itemref.attrib.get("idref", "")
			item = manifest.get(idref)
			if not item:
				continue
			href, media = item
			if media in DOC_MEDIA_TYPES:
				full_path = posixpath.normpath(posixpath.join(opf_dir, href))
				doc_paths.append(full_path)

		if not doc_paths:
			# Fallback when spine is missing or malformed.
			for href, media in manifest.values():
				if media in DOC_MEDIA_TYPES:
					doc_paths.append(posixpath.normpath(posixpath.join(opf_dir, href)))

		chapters: list[str] = []
		for doc_path in doc_paths:
			try:
				raw = zf.read(doc_path)
			except KeyError:
				continue
			parser = HTMLToMarkdownParser()
			parser.feed(_decode_xml(raw))
			md = parser.get_markdown().strip()
			if md:
				chapters.append(md)

		return metadata, chapters


def compose_markdown(metadata: EpubMetadata, chapters: Iterable[str]) -> str:
	chapter_list = list(chapters)
	parts: list[str] = []

	if metadata.title:
		parts.append(f"# {metadata.title}\n")
	if metadata.creator:
		parts.append(f"**Author:** {metadata.creator}\n")
	if metadata.language:
		parts.append(f"**Language:** {metadata.language}\n")
	if parts:
		parts.append("\n")

	for idx, ch in enumerate(chapter_list, start=1):
		if len(chapter_list) > 1:
			parts.append(f"## Chapter {idx}\n\n")
		parts.append(ch.strip())
		parts.append("\n\n")

	return collapse_blank_lines("".join(parts))


def convert_epub_to_markdown(epub_path: Path, output_path: Path) -> None:
	metadata, chapters = read_epub_documents(epub_path)
	if not chapters:
		raise ValueError("No readable XHTML/HTML content found in EPUB")
	markdown = compose_markdown(metadata, chapters)
	output_path.write_text(markdown, encoding="utf-8")


def default_output_path(epub_path: Path) -> Path:
	return epub_path.with_suffix(".md")


def build_arg_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Convert EPUB to Markdown")
	parser.add_argument("input", type=Path, help="Path to the input .epub file")
	parser.add_argument(
		"-o",
		"--output",
		type=Path,
		help="Path to output .md file (default: same name as input)",
	)
	return parser


def main() -> int:
	parser = build_arg_parser()
	args = parser.parse_args()

	input_path: Path = args.input
	output_path: Path = args.output or default_output_path(input_path)

	if not input_path.exists():
		print(f"Input file not found: {input_path}", file=sys.stderr)
		return 1
	if input_path.suffix.lower() != ".epub":
		print("Input file must have .epub extension", file=sys.stderr)
		return 1

	try:
		convert_epub_to_markdown(input_path, output_path)
	except (zipfile.BadZipFile, ET.ParseError, ValueError, OSError) as exc:
		print(f"Conversion failed: {exc}", file=sys.stderr)
		return 1

	print(f"Markdown generated: {output_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
