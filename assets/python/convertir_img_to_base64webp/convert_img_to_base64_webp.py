from __future__ import annotations

import argparse
import base64
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image


@dataclass
class ConversionResult:
	webp_bytes: bytes
	width: int
	height: int
	quality: int


def parse_height(value: str) -> int | None:
	if value.lower() == "original":
		return None

	height = int(value)
	if height <= 0:
		raise argparse.ArgumentTypeError("height debe ser un entero positivo o 'original'")
	return height


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Convierte una imagen a WebP comprimido y devuelve un bloque Markdown "
			"con data URI lista para pegar en un fichero .md"
		)
	)
	parser.add_argument("image", help="Ruta de la imagen de entrada")
	parser.add_argument(
		"-k",
		"--max-kb",
		type=int,
		default=50,
		help="Tamano maximo aproximado del WebP en KB (por defecto: 50)",
	)
	parser.add_argument(
		"-q",
		"--quality-start",
		type=int,
		default=80,
		help="Calidad inicial WebP (por defecto: 80)",
	)
	parser.add_argument(
		"--quality-min",
		type=int,
		default=35,
		help="Calidad minima antes de reducir dimensiones (por defecto: 35)",
	)
	parser.add_argument(
		"--resize-step",
		type=float,
		default=0.9,
		help="Factor de reduccion de dimensiones por iteracion (por defecto: 0.9)",
	)
	parser.add_argument(
		"--min-width",
		type=int,
		default=320,
		help="Anchura minima permitida al reducir (por defecto: 320)",
	)
	parser.add_argument(
		"--height",
		type=parse_height,
		default=500,
		help="Altura inicial en px (por defecto: 500). Usa 'original' para mantener la altura original",
	)
	parser.add_argument(
		"--alt",
		default=None,
		help="Texto alt del bloque Markdown. Si se omite, usa el nombre del archivo",
	)
	parser.add_argument(
		"-o",
		"--output",
		type=Path,
		default=Path("converted_base64.txt"),
		help="Guarda el resultado de texto en este archivo (por defecto: converted_base64.txt)",
	)
	parser.add_argument(
		"--save-webp",
		type=Path,
		help="Guarda tambien el WebP optimizado en esta ruta",
	)
	return parser.parse_args()


def normalize_image(image: Image.Image) -> Image.Image:
	if image.mode in {"RGB", "RGBA"}:
		return image
	if "A" in image.getbands():
		return image.convert("RGBA")
	return image.convert("RGB")


def resize_to_height(image: Image.Image, target_height: int | None) -> Image.Image:
	if target_height is None or image.height == target_height:
		return image

	target_width = max(int(image.width * (target_height / image.height)), 1)
	return image.resize((target_width, target_height), Image.Resampling.LANCZOS)


def encode_webp(image: Image.Image, quality: int) -> bytes:
	buffer = BytesIO()
	image.save(buffer, format="WEBP", quality=quality, method=6)
	return buffer.getvalue()


def fit_to_size(
	image: Image.Image,
	max_kb: int,
	quality_start: int,
	quality_min: int,
	resize_step: float,
	min_width: int,
	target_height: int | None,
) -> ConversionResult:
	if max_kb <= 0:
		raise ValueError("max_kb debe ser mayor que 0")
	if not 0 < resize_step < 1:
		raise ValueError("resize_step debe estar entre 0 y 1")
	if not 1 <= quality_min <= quality_start <= 100:
		raise ValueError("quality_min y quality_start deben estar entre 1 y 100")

	target_bytes = max_kb * 1024
	working = resize_to_height(normalize_image(image), target_height)
	best_result: ConversionResult | None = None

	while True:
		for quality in range(quality_start, quality_min - 1, -5):
			webp_bytes = encode_webp(working, quality)
			current = ConversionResult(
				webp_bytes=webp_bytes,
				width=working.width,
				height=working.height,
				quality=quality,
			)
			if best_result is None or len(webp_bytes) < len(best_result.webp_bytes):
				best_result = current
			if len(webp_bytes) <= target_bytes:
				return current

		next_width = max(int(working.width * resize_step), min_width)
		if next_width >= working.width or working.width <= min_width:
			return best_result

		next_height = max(int(working.height * (next_width / working.width)), 1)
		working = working.resize((next_width, next_height), Image.Resampling.LANCZOS)


def build_markdown(data_uri: str, alt_text: str) -> str:
	return f"![{alt_text}]({data_uri})"


def main() -> int:
	args = parse_args()
	image_path = Path(args.image).expanduser().resolve()
	if not image_path.is_file():
		raise FileNotFoundError(f"No existe la imagen: {image_path}")

	with Image.open(image_path) as source_image:
		result = fit_to_size(
			image=source_image,
			max_kb=args.max_kb,
			quality_start=args.quality_start,
			quality_min=args.quality_min,
			resize_step=args.resize_step,
			min_width=args.min_width,
			target_height=args.height,
		)

	encoded = base64.b64encode(result.webp_bytes).decode("ascii")
	data_uri = f"data:image/webp;base64,{encoded}"
	alt_text = args.alt or image_path.stem
	markdown = build_markdown(data_uri, alt_text)

	if args.save_webp:
		args.save_webp.write_bytes(result.webp_bytes)

	if args.output:
		args.output.write_text(markdown, encoding="utf-8")

	print(markdown)
	print(
		f"\nTamano final: {len(result.webp_bytes) / 1024:.1f} KB | "
		f"{result.width}x{result.height} | quality={result.quality}"
		,
		file=sys.stderr,
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
