import shutil
import subprocess
from pathlib import Path


INPUT_DIR = Path(r"D:\AlexPersonal\OPOS25\SETA\audios_m4a")
OUTPUT_DIR = INPUT_DIR / "mp3_64k"
HIST_DIR = INPUT_DIR / "historicos_convertidos"

# Si no tienes ffmpeg en PATH, pon la ruta completa:
# FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
FFMPEG = "ffmpeg"

BITRATE = "64k"


def convertir_m4a_a_mp3(m4a_path: Path, mp3_path: Path):
    cmd = [
        str(FFMPEG),
        "-y",
        "-i", str(m4a_path),
        "-c:a", "libmp3lame",
        "-b:a", BITRATE,
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True)


def main():
    if not INPUT_DIR.exists():
        print(f"❌ No existe la carpeta: {INPUT_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    HIST_DIR.mkdir(parents=True, exist_ok=True)

    m4as = list(INPUT_DIR.glob("*.m4a"))
    if not m4as:
        print(f"❌ No se han encontrado .m4a en: {INPUT_DIR}")
        return

    print(f"🎧 Audios encontrados: {len(m4as)}")
    print("----")

    for m4a in m4as:
        nombre = m4a.stem
        mp3 = OUTPUT_DIR / f"{nombre}.mp3"

        print(f"➡️ Procesando: {m4a.name}")

        try:
            convertir_m4a_a_mp3(m4a, mp3)
            print(f"   ✅ OK -> {mp3.name}")

            # Mover el M4A a históricos (solo si OK)
            destino_m4a = HIST_DIR / m4a.name
            shutil.move(str(m4a), str(destino_m4a))
            print(f"   📦 M4A movido a: {destino_m4a}")

        except subprocess.CalledProcessError:
            print(f"   ❌ ERROR convirtiendo {m4a.name} (no se mueve el M4A)")

    print("----")
    print("✅ Terminado.")


if __name__ == "__main__":
    main()
