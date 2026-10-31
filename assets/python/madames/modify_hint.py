import argparse
import json
import os
from pathlib import Path


DIRECTORY = Path(__file__).resolve().parent


def migrate_file(path, dry_run=False):
	with path.open("r", encoding="utf-8-sig") as source:
		questions = json.load(source)
	if not isinstance(questions, list):
		raise ValueError("el contenido JSON debe ser un array")

	changes = []
	for index, question in enumerate(questions, start=1):
		if not isinstance(question, dict):
			raise ValueError(f"pregunta {index}: el elemento debe ser un objeto")
		if "hint" not in question:
			continue

		hint = question["hint"]
		if not isinstance(hint, str):
			raise ValueError(f"pregunta {index}: hint debe ser texto")
		options = question.get("answerOptions")
		if not isinstance(options, list):
			raise ValueError(f"pregunta {index}: answerOptions debe ser un array")
		correct_options = [
			option for option in options
			if isinstance(option, dict) and option.get("isCorrect") is True
		]
		if len(correct_options) != 1:
			raise ValueError(
				f"pregunta {index}: se esperaba exactamente una respuesta correcta"
			)

		correct_option = correct_options[0]
		if "rationale" in correct_option and correct_option["rationale"] != hint:
			raise ValueError(
				f"pregunta {index}: ya existe un rationale distinto al hint"
			)
		changes.append((question, correct_option, hint))

	if dry_run or not changes:
		return len(changes)

	for question, correct_option, hint in changes:
		correct_option["rationale"] = hint
		del question["hint"]

	temporary_path = path.with_suffix(path.suffix + ".tmp")
	try:
		with temporary_path.open("w", encoding="utf-8") as destination:
			json.dump(questions, destination, ensure_ascii=False, indent=2)
			destination.write("\n")
		os.chmod(temporary_path, path.stat().st_mode)
		os.replace(temporary_path, path)
	finally:
		temporary_path.unlink(missing_ok=True)

	return len(changes)


def main():
	parser = argparse.ArgumentParser(
		description="Mueve el hint al rationale de la respuesta correcta."
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="informa de los cambios sin modificar los archivos",
	)
	args = parser.parse_args()
	paths = sorted(DIRECTORY.glob("*_MADAMES.json"))
	if not paths:
		print(f"No se encontraron archivos *_MADAMES.json en {DIRECTORY}")
		return 1

	failed = False
	for path in paths:
		try:
			changed = migrate_file(path, dry_run=args.dry_run)
			status = "se migrarían" if args.dry_run else "migradas"
			print(f"{path.name}: {changed} preguntas {status}")
		except (OSError, json.JSONDecodeError, ValueError) as error:
			failed = True
			print(f"ERROR {path.name}: {error}")

	return int(failed)


if __name__ == "__main__":
	raise SystemExit(main())
