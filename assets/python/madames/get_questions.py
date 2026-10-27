import json
import re
import time
import unicodedata
from pathlib import Path
from uuid import uuid4

import requests
from bs4 import BeautifulSoup


N_CALLS = 4
SUBJECT_ID = "T17"
PAUSE_SECONDS = 3
TIMEOUT_SECONDS = 30
ENDPOINT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
COOKIES = {
	"PHPSESSID": "dtp21l9r4g9h11fcoq3bh4u1ft",
	"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx": "23c24a36844b10aeb62cd5b527cb684e",
	"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx": "23c24a36844b10aeb62cd5b527cb684e",
}
REQUEST_DATA = {
	"accion": "autoevaluacionEjercicioAPersonalizado",
	"temas": "107",
	"modopreguntas": "undefined",
	"numPreguntas": "30",
}
HEADERS = {
	"User-Agent": "Mozilla/5.0",
	"Accept": "application/json, text/javascript, */*; q=0.01",
	"Referer": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
	"Origin": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
	"X-Requested-With": "XMLHttpRequest",
}
OUTPUT_DIRECTORY = Path(__file__).resolve().parent


def clean_text(element):
	return " ".join(element.get_text(" ", strip=True).split())


def question_key(text):
	return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def parse_questions(payload, subject_id):
	if payload.get("error") != 0:
		raise ValueError(f"El endpoint devuelve error: {payload.get('error')}")
	markup = payload.get("htmlRespuesta")
	if not isinstance(markup, str) or not markup.strip():
		raise ValueError("La respuesta no contiene htmlRespuesta")
	document = BeautifulSoup(markup, "html.parser")
	containers = document.select('div.ejerContent[id^="pregunta-A-"]')
	if not containers:
		raise ValueError("No hay preguntas en la respuesta; comprueba la sesion")

	questions = []
	for container in containers:
		source_id = container["id"].removeprefix("pregunta-A-")
		statement = container.select_one(".texto-enunciado strong div")
		if statement is None:
			raise ValueError(f"Pregunta {source_id}: falta el enunciado")
		options = []
		for item in container.select("ul.lista-respuestas > li"):
			label = item.select_one("label")
			if label is None:
				raise ValueError(f"Pregunta {source_id}: falta una opcion")
			options.append({
				"text": re.sub(r"^[a-dA-D][.)]\s*", "", clean_text(label)),
				"isCorrect": item.select_one("img.respuesta_correcta") is not None,
			})
		if len(options) != 4 or sum(option["isCorrect"] for option in options) != 1:
			raise ValueError(f"Pregunta {source_id}: se requieren 4 opciones y 1 correcta")
		explanation = container.select_one(".texto-explicacion")
		if explanation is None:
			raise ValueError(f"Pregunta {source_id}: falta la explicacion")
		question = {
			"guid": f"{uuid4()}-{source_id}",
			"subjectId": subject_id,
			"origin": "madames",
			"type": "test",
			"question": clean_text(statement),
			"answerOptions": options,
			"hint": clean_text(explanation),
		}
		if not question["question"] or any(not option["text"] for option in options):
			raise ValueError(f"Pregunta {source_id}: hay textos vacios")
		questions.append((source_id, question))
	return questions


def add_unique_questions(parsed, questions, seen_ids, seen_texts):
	added = 0
	for source_id, question in parsed:
		text_key = question_key(question["question"])
		duplicate = source_id in seen_ids or text_key in seen_texts
		seen_ids.add(source_id)
		seen_texts.add(text_key)
		if not duplicate:
			questions.append(question)
			added += 1
	return added


def load_questions(output_path):
	questions = []
	seen_ids = set()
	seen_texts = set()
	if not output_path.exists():
		return questions, seen_ids, seen_texts
	existing = json.loads(output_path.read_text(encoding="utf-8-sig"))
	if not isinstance(existing, list):
		raise ValueError(f"{output_path}: el JSON existente debe ser un array")
	for index, question in enumerate(existing, start=1):
		if (
			not isinstance(question, dict)
			or not isinstance(question.get("question"), str)
			or not question["question"].strip()
			or not isinstance(question.get("guid"), str)
		):
			raise ValueError(f"{output_path}: pregunta existente {index} no valida")
		guid_match = re.fullmatch(
			r"[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}-(\d+)",
			question["guid"],
		)
		if guid_match:
			seen_ids.add(guid_match.group(1))
		seen_texts.add(question_key(question["question"]))
		questions.append(question)
	return questions, seen_ids, seen_texts


def save_questions(output_path, questions):
	temporary_path = output_path.with_suffix(".tmp")
	temporary_path.write_text(
		json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
		encoding="utf-8",
	)
	temporary_path.replace(output_path)


def main():
	if not isinstance(N_CALLS, int) or isinstance(N_CALLS, bool) or N_CALLS < 1:
		raise ValueError("N_CALLS debe ser un entero positivo")
	if PAUSE_SECONDS < 0 or TIMEOUT_SECONDS <= 0:
		raise ValueError("PAUSE_SECONDS debe ser >= 0 y TIMEOUT_SECONDS > 0")
	if not SUBJECT_ID.strip() or SUBJECT_ID == "TXX":
		raise ValueError("Configura SUBJECT_ID al inicio del script")
	if not COOKIES.get("PHPSESSID"):
		raise ValueError("Configura COOKIES con una sesion vigente del request de ejemplo")

	OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
	output_path = OUTPUT_DIRECTORY / f"{SUBJECT_ID}_MADAMES.json"
	questions, seen_ids, seen_texts = load_questions(output_path)
	print(f"Cargadas {len(questions)} preguntas existentes de {output_path}")
	failures = 0
	interrupted = False
	try:
		with requests.Session() as session:
			session.headers.update(HEADERS)
			session.cookies.update(COOKIES)
			for call_number in range(1, N_CALLS + 1):
				if call_number > 1:
					time.sleep(PAUSE_SECONDS)
				try:
					response = session.post(
						ENDPOINT, data=REQUEST_DATA, timeout=TIMEOUT_SECONDS
					)
					response.raise_for_status()
					payload = json.loads(response.content.decode("utf-8-sig"))
					if not isinstance(payload, dict):
						raise ValueError("La respuesta JSON no es un objeto")
					parsed = parse_questions(payload, SUBJECT_ID)
				except (requests.RequestException, ValueError) as error:
					failures += 1
					print(f"Llamada {call_number}/{N_CALLS}: fallo sin reintento: {error}")
					continue
				added = add_unique_questions(parsed, questions, seen_ids, seen_texts)
				save_questions(output_path, questions)
				print(
					f"Llamada {call_number}/{N_CALLS}: {len(parsed)} recibidas, "
					f"{added} nuevas, {len(parsed) - added} duplicadas; "
					f"total {len(questions)}"
				)
	except KeyboardInterrupt:
		interrupted = True
		print("Interrumpido; guardando preguntas acumuladas")
	finally:
		save_questions(output_path, questions)
		print(f"Guardadas {len(questions)} preguntas en {output_path}. Fallos: {failures}")
	return 130 if interrupted else int(failures > 0)


if __name__ == "__main__":
	raise SystemExit(main())
