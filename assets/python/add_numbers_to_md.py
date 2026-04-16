from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADING_RE = re.compile(r"^( {0,3})(#{1,6})\s+(.*?)\s*$")
NUMBER_PREFIX_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Añade numeración jerárquica a los títulos Markdown y pide "
			"confirmación interactiva en cada encabezado."
		)
	)
	parser.add_argument("markdown_file", help="Ruta del fichero Markdown a modificar")
	parser.add_argument(
		"start_number",
		help="Número inicial para el primer encabezado, por ejemplo: 5.1",
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
	clean_title = strip_existing_number(title)
	return f"{indent}{hashes} {format_number(number_parts)} {clean_title}"


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


def process_markdown(markdown_path: Path, start_number: list[int]) -> None:
	original_text = markdown_path.read_text(encoding="utf-8-sig")
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

	if new_text == original_text:
		print("No se han realizado cambios.")
		return

	markdown_path.write_text(new_text, encoding="utf-8")
	print(f"Fichero actualizado: {markdown_path}")


def main() -> int:
	args = parse_args()
	markdown_path = Path(args.markdown_file).expanduser().resolve()

	if not markdown_path.exists():
		print(f"No existe el fichero: {markdown_path}")
		return 1

	if markdown_path.suffix.lower() != ".md":
		print(f"El fichero no parece Markdown: {markdown_path}")
		return 1

	try:
		start_number = parse_number(args.start_number)
	except ValueError as error:
		print(error)
		return 1

	process_markdown(markdown_path, start_number)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
