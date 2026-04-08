import argparse
import os
import re
import shutil
import subprocess
import sys


ADMONITION_LABELS = {
	"NOTE": "Nota",
	"TIP": "Consejo",
	"IMPORTANT": "Importante",
	"WARNING": "Aviso",
	"CAUTION": "Precaucion",
}


def replace_inline_markup(text):
	text = re.sub(r"image::([^\[]+)\[(.*?)\]", lambda match: f"![{match.group(2) or os.path.basename(match.group(1))}]({match.group(1)})", text)
	text = re.sub(r"link:([^\[]+)\[(.*?)\]", lambda match: f"[{match.group(2) or match.group(1)}]({match.group(1)})", text)
	text = re.sub(r"xref:([^\[]+)\[(.*?)\]", lambda match: f"[{match.group(2) or match.group(1)}]({match.group(1)})", text)
	text = re.sub(r"<<([^,>]+),?([^>]*)>>", lambda match: f"[{match.group(2) or match.group(1)}](#{slugify(match.group(1))})", text)
	text = re.sub(r"\+([^+\n]+)\+", r"`\1`", text)
	return text


def slugify(value):
	slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
	return slug or "seccion"


def convert_with_pandoc(input_path, output_path):
	pandoc_path = shutil.which("pandoc")
	if not pandoc_path:
		return False

	command = [
		pandoc_path,
		"--from",
		"asciidoc",
		"--to",
		"gfm",
		"--wrap=none",
		"--output",
		output_path,
		input_path,
	]

	result = subprocess.run(command, capture_output=True, text=True)
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or "Pandoc ha fallado durante la conversion")

	return True


def convert_with_simple_rules(content):
	output_lines = []
	pending_block_type = None
	pending_source_lang = ""
	in_code_block = False
	in_quote_block = False

	for raw_line in content.splitlines():
		line = raw_line.rstrip()
		stripped = line.strip()

		if not in_code_block and not in_quote_block and re.match(r"^:[a-z0-9_-]+:\s*.*$", stripped, flags=re.IGNORECASE):
			continue

		source_match = re.match(r"^\[source(?:,\s*([^\],]+))?.*\]$", stripped, flags=re.IGNORECASE)
		if not in_code_block and source_match:
			pending_block_type = "source"
			pending_source_lang = (source_match.group(1) or "").strip()
			continue

		if not in_code_block and re.match(r"^\[(quote|verse)\].*$", stripped, flags=re.IGNORECASE):
			pending_block_type = "quote"
			continue

		if stripped in {"----", "...."}:
			if in_code_block:
				output_lines.append("```")
				in_code_block = False
			else:
				language = pending_source_lang if pending_block_type == "source" else ""
				output_lines.append(f"```{language}".rstrip())
				in_code_block = True
			pending_block_type = None
			pending_source_lang = ""
			continue

		if stripped == "____":
			in_quote_block = not in_quote_block
			pending_block_type = None
			continue

		if in_code_block:
			output_lines.append(raw_line)
			continue

		heading_match = re.match(r"^(={1,6})\s+(.*)$", line)
		if heading_match:
			level = len(heading_match.group(1))
			output_lines.append(f"{'#' * level} {replace_inline_markup(heading_match.group(2).strip())}")
			continue

		admonition_match = re.match(r"^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):\s*(.*)$", stripped)
		if admonition_match:
			label = ADMONITION_LABELS.get(admonition_match.group(1), admonition_match.group(1).title())
			body = replace_inline_markup(admonition_match.group(2))
			output_lines.append(f"> **{label}:** {body}".rstrip())
			continue

		image_match = re.match(r"^image::([^\[]+)\[(.*?)\]$", stripped)
		if image_match:
			alt_text = image_match.group(2) or os.path.basename(image_match.group(1))
			output_lines.append(f"![{alt_text}]({image_match.group(1)})")
			continue

		ordered_match = re.match(r"^(\s*)\.\s+(.*)$", line)
		if ordered_match:
			output_lines.append(f"{ordered_match.group(1)}1. {replace_inline_markup(ordered_match.group(2))}")
			continue

		if in_quote_block:
			quoted_line = replace_inline_markup(line)
			output_lines.append(f"> {quoted_line}" if quoted_line else ">")
			continue

		output_lines.append(replace_inline_markup(line))

	if in_code_block:
		output_lines.append("```")

	return "\n".join(output_lines) + "\n"


def convert_adoc_to_markdown(input_path, output_path, engine="auto"):
	if not os.path.isfile(input_path):
		raise FileNotFoundError(f"No existe el fichero: {input_path}")

	if not input_path.lower().endswith(".adoc"):
		raise ValueError("El fichero de entrada debe tener extension .adoc")

	if engine in {"auto", "pandoc"}:
		used_pandoc = convert_with_pandoc(input_path, output_path)
		if used_pandoc:
			return "pandoc"
		if engine == "pandoc":
			raise RuntimeError("No se ha encontrado pandoc en el sistema")

	with open(input_path, "r", encoding="utf-8-sig") as source_file:
		content = source_file.read()

	markdown_content = convert_with_simple_rules(content)

	with open(output_path, "w", encoding="utf-8", newline="\n") as target_file:
		target_file.write(markdown_content)

	return "simple"


def build_output_path(input_path, output_path=None):
	if output_path:
		return output_path
	base_name, _ = os.path.splitext(input_path)
	return f"{base_name}.md"


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Convierte un fichero AsciiDoc (.adoc) a Markdown (.md)"
	)
	parser.add_argument("entrada", help="Ruta del fichero .adoc")
	parser.add_argument("salida", nargs="?", help="Ruta del fichero .md de salida")
	parser.add_argument(
		"--engine",
		choices=["auto", "pandoc", "simple"],
		default="auto",
		help="Motor de conversion: auto intenta pandoc y, si no existe, usa el conversor interno",
	)

	args = parser.parse_args()

	input_file = os.path.abspath(args.entrada)
	output_file = os.path.abspath(build_output_path(input_file, args.salida))

	try:
		engine_used = convert_adoc_to_markdown(input_file, output_file, args.engine)
		print(f"Markdown generado correctamente en: {output_file}")
		print(f"Motor utilizado: {engine_used}")
	except Exception as exc:
		print(f"Error: {exc}")
		sys.exit(1)
