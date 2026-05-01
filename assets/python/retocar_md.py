from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path


HEADING_RE = re.compile(r"^( {0,3})(#{1,6})\s+(.*?)\s*$")
NUMBER_PREFIX_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")
ANCHOR_SUFFIX_RE = re.compile(r"\s*<a id=\"[^\"]+\"></a>\s*$")
PLACEHOLDER_RE = re.compile(r"^\s*INDICE INTERACTIVO\s*$", re.IGNORECASE)

TOC_START = "<!-- TOC START -->"
TOC_END = "<!-- TOC END -->"


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Añade numeración jerárquica a los títulos Markdown y puede "
			"generar un índice clicable al principio del documento."
		)
	)
	parser.add_argument("markdown_file", help="Ruta del fichero Markdown a modificar")
	parser.add_argument(
		"start_number",
		nargs="?",
		help="Número inicial para el primer encabezado, por ejemplo: 5.1",
	)
	parser.add_argument(
		"--toc",
		action="store_true",
		help="Genera o actualiza un índice clicable con enlaces internos.",
	)
	parser.add_argument(
		"--corregirHeaders",
		action="store_true",
		help=(
			"Detecta saltos inválidos en la jerarquía de encabezados, por ejemplo "
			"de ## a ####, y propone corregirlos de forma interactiva."
		),
	)
	return parser.parse_args()


def parse_number(text: str) -> list[int]:
	cleaned = text.strip().rstrip(".")
	if not cleaned or not re.fullmatch(r"\d+(?:\.\d+)*", cleaned):
		raise ValueError(f"Número no válido: {text!r}")

	parts = [int(part) for part in cleaned.split(".")]
	if any(part < 0 for part in parts):
		raise ValueError(f"Número no válido: {text!r}")
	return parts


def format_number(parts: list[int]) -> str:
	return ".".join(str(part) for part in parts)


def strip_existing_number(title: str) -> str:
	return NUMBER_PREFIX_RE.sub("", title).strip()


def strip_existing_anchor(title: str) -> str:
	return ANCHOR_SUFFIX_RE.sub("", title).strip()


def build_candidate_number(
	base_number: list[int],
	accepted_numbers_by_level: dict[int, list[int]],
	current_level: int,
) -> list[int]:
	if current_level in accepted_numbers_by_level:
		candidate = accepted_numbers_by_level[current_level].copy()
		candidate[-1] += 1
		return candidate

	parent_levels = [level for level in accepted_numbers_by_level if level < current_level]
	if not parent_levels:
		return base_number.copy()

	parent_level = max(parent_levels)
	candidate = accepted_numbers_by_level[parent_level].copy()
	candidate.extend([1] * (current_level - parent_level))
	return candidate


def apply_number_to_heading(line: str, number_parts: list[int]) -> str:
	match = HEADING_RE.match(line)
	if not match:
		return line

	indent, hashes, title = match.groups()
	clean_title = strip_existing_number(strip_existing_anchor(title))
	return f"{indent}{hashes} {format_number(number_parts)} {clean_title}"


def apply_heading_level_to_line(line: str, new_level: int) -> str:
	match = HEADING_RE.match(line)
	if not match:
		return line

	indent, _hashes, title = match.groups()
	return f"{indent}{'#' * new_level} {title}"


def prompt_user(
	line_number: int,
	line: str,
	candidate_number: list[int],
) -> tuple[str, list[int] | None]:
	new_line = apply_number_to_heading(line, candidate_number)
	print()
	print(f"Línea {line_number}")
	print(f"Actual   : {line}")
	print(f"Propuesta: {new_line}")
	answer = input("Enter=aceptar, s=saltar, o escribe un número: ").strip()

	if answer == "":
		return new_line, candidate_number

	if answer.lower() == "s":
		return line, None

	override_number = parse_number(answer)
	return apply_number_to_heading(line, override_number), override_number


def prompt_header_correction(
	line_number: int,
	line: str,
	current_level: int,
	expected_level: int,
) -> tuple[str, int]:
	new_line = apply_heading_level_to_line(line, expected_level)
	print()
	print(f"Línea {line_number}")
	print(f"Jerarquía detectada: nivel {current_level} después de nivel {expected_level - 1}")
	print(f"Actual   : {line}")
	print(f"Propuesta: {new_line}")
	print("La corrección se aplicará también a los encabezados dependientes hasta el siguiente nivel equivalente o superior.")
	answer = input("Enter=aceptar, s=saltar, o escribe un nivel 1-6: ").strip()

	if answer == "":
		return new_line, expected_level

	if answer.lower() == "s":
		return line, current_level

	if not answer.isdigit():
		raise ValueError(f"Nivel no válido: {answer!r}")

	override_level = int(answer)
	if override_level < 1 or override_level > 6:
		raise ValueError(f"Nivel no válido: {answer!r}")

	return apply_heading_level_to_line(line, override_level), override_level


def process_markdown_header_corrections(original_text: str) -> str:
	lines = original_text.splitlines()
	trailing_newline = original_text.endswith(("\n", "\r"))

	updated_lines: list[str] = []
	inside_fenced_block = False
	last_heading_level = 0
	active_level_shift = 0
	active_boundary_level = 0

	for line_number, line in enumerate(lines, start=1):
		stripped = line.lstrip()
		if stripped.startswith("```") or stripped.startswith("~~~"):
			inside_fenced_block = not inside_fenced_block
			updated_lines.append(line)
			continue

		match = HEADING_RE.match(line)
		if inside_fenced_block or not match:
			updated_lines.append(line)
			continue

		raw_level = len(match.group(2))
		if active_level_shift and raw_level <= active_boundary_level:
			active_level_shift = 0
			active_boundary_level = 0

		current_level = raw_level + active_level_shift if active_level_shift else raw_level
		if last_heading_level and current_level > last_heading_level + 1:
			expected_level = last_heading_level + 1
			try:
				updated_line, accepted_level = prompt_header_correction(
					line_number=line_number,
					line=line,
					current_level=current_level,
					expected_level=expected_level,
				)
			except ValueError as error:
				print(f"Entrada inválida en la línea {line_number}: {error}")
				print("Se deja el encabezado sin cambios.")
				updated_lines.append(line)
				last_heading_level = current_level
				continue

			updated_lines.append(updated_line)
			active_level_shift = accepted_level - raw_level
			active_boundary_level = accepted_level if active_level_shift else 0
			last_heading_level = accepted_level
			continue

		updated_line = apply_heading_level_to_line(line, current_level) if current_level != raw_level else line
		updated_lines.append(updated_line)
		last_heading_level = current_level

	new_text = "\n".join(updated_lines)
	if trailing_newline:
		new_text += "\n"
	return new_text


def process_markdown_text(original_text: str, start_number: list[int]) -> str:
	lines = original_text.splitlines()
	trailing_newline = original_text.endswith(("\n", "\r"))

	updated_lines: list[str] = []
	accepted_numbers_by_level: dict[int, list[int]] = {}
	inside_fenced_block = False

	for line_number, line in enumerate(lines, start=1):
		stripped = line.lstrip()
		if stripped.startswith("```") or stripped.startswith("~~~"):
			inside_fenced_block = not inside_fenced_block
			updated_lines.append(line)
			continue

		match = HEADING_RE.match(line)
		if inside_fenced_block or not match:
			updated_lines.append(line)
			continue

		current_level = len(match.group(2))
		candidate_number = build_candidate_number(
			base_number=start_number,
			accepted_numbers_by_level=accepted_numbers_by_level,
			current_level=current_level,
		)

		try:
			updated_line, accepted_number = prompt_user(
				line_number=line_number,
				line=line,
				candidate_number=candidate_number,
			)
		except ValueError as error:
			print(f"Entrada inválida en la línea {line_number}: {error}")
			print("Se deja la línea sin cambios.")
			updated_lines.append(line)
			continue

		updated_lines.append(updated_line)
		if accepted_number is not None:
			accepted_numbers_by_level[current_level] = accepted_number
			for level in list(accepted_numbers_by_level):
				if level > current_level:
					del accepted_numbers_by_level[level]

	new_text = "\n".join(updated_lines)
	if trailing_newline:
		new_text += "\n"
	return new_text


def slugify(value: str) -> str:
	normalized = unicodedata.normalize("NFKD", value)
	without_accents = "".join(
		character for character in normalized if not unicodedata.combining(character)
	)
	slug = re.sub(r"[^a-zA-Z0-9]+", "-", without_accents.lower()).strip("-")
	return slug or "section"


def make_unique_anchor_id(base_text: str, used_ids: set[str]) -> str:
	base_id = slugify(base_text)
	anchor_id = base_id
	suffix = 2
	while anchor_id in used_ids:
		anchor_id = f"{base_id}-{suffix}"
		suffix += 1
	used_ids.add(anchor_id)
	return anchor_id


def build_toc_entry(level: int, heading_text: str, anchor_id: str, min_level: int) -> str:
	indent = "  " * max(level - min_level, 0)
	return f"{indent}- [{heading_text}](#{anchor_id})"


def replace_toc_block(lines: list[str], toc_block: list[str]) -> list[str]:
	start_index = None
	end_index = None
	for index, line in enumerate(lines):
		if line.strip() == TOC_START:
			start_index = index
		if line.strip() == TOC_END:
			end_index = index
			break

	if start_index is not None and end_index is not None and start_index <= end_index:
		return lines[:start_index] + toc_block + lines[end_index + 1 :]

	for index, line in enumerate(lines):
		if PLACEHOLDER_RE.match(line):
			return lines[:index] + toc_block + lines[index + 1 :]

	return toc_block + [""] + lines


def generate_toc_text(original_text: str) -> str:
	lines = original_text.splitlines()
	trailing_newline = original_text.endswith(("\n", "\r"))
	working_lines: list[str] = []
	heading_entries: list[tuple[int, str, str]] = []
	used_ids: set[str] = set()
	inside_fenced_block = False
	inside_toc_block = False

	for line in lines:
		stripped = line.strip()
		if stripped == TOC_START:
			inside_toc_block = True
			continue
		if stripped == TOC_END:
			inside_toc_block = False
			continue
		if inside_toc_block:
			continue

		check_line = line.lstrip()
		if check_line.startswith("```") or check_line.startswith("~~~"):
			inside_fenced_block = not inside_fenced_block
			working_lines.append(line)
			continue

		match = HEADING_RE.match(line)
		if inside_fenced_block or not match:
			working_lines.append(line)
			continue

		indent, hashes, title = match.groups()
		heading_text = strip_existing_anchor(title)
		anchor_id = make_unique_anchor_id(heading_text, used_ids)
		working_lines.append(f"{indent}{hashes} {heading_text} <a id=\"{anchor_id}\"></a>")
		heading_entries.append((len(hashes), heading_text, anchor_id))

	if not heading_entries:
		return original_text

	min_level = min(level for level, _, _ in heading_entries)
	toc_lines = [build_toc_entry(level, heading_text, anchor_id, min_level) for level, heading_text, anchor_id in heading_entries]
	toc_block = [
		TOC_START,
		"**INDICE INTERACTIVO**",
		"",
		*toc_lines,
		TOC_END,
	]
	final_lines = replace_toc_block(working_lines, toc_block)
	new_text = "\n".join(final_lines)
	if trailing_newline:
		new_text += "\n"
	return new_text


def main() -> int:
	args = parse_args()
	markdown_path = Path(args.markdown_file).expanduser().resolve()

	if not markdown_path.exists():
		print(f"No existe el fichero: {markdown_path}")
		return 1

	if markdown_path.suffix.lower() != ".md":
		print(f"El fichero no parece Markdown: {markdown_path}")
		return 1

	if not args.start_number and not args.toc:
		if not args.corregirHeaders:
			print("Debes indicar un número inicial, usar --toc o usar --corregirHeaders.")
			return 1

	original_text = markdown_path.read_text(encoding="utf-8-sig")
	updated_text = original_text

	if args.corregirHeaders:
		updated_text = process_markdown_header_corrections(updated_text)

	if args.start_number:
		try:
			start_number = parse_number(args.start_number)
		except ValueError as error:
			print(error)
			return 1
		updated_text = process_markdown_text(updated_text, start_number)

	if args.toc:
		updated_text = generate_toc_text(updated_text)

	if updated_text == original_text:
		print("No se han realizado cambios.")
		return 0

	markdown_path.write_text(updated_text, encoding="utf-8")
	print(f"Fichero actualizado: {markdown_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
