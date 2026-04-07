import subprocess
from pathlib import Path


# ========= CONFIG =========
INPUT_DIR = Path(r"D:\AlexPersonal\OPOS25\SETA\audios_m4a\mp3_64k")
OUTPUT_DIR = INPUT_DIR / "mp4_youtube"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Si no tienes ffmpeg en PATH, pon la ruta completa:
# FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
FFMPEG = "ffmpeg"

# Si pones una imagen, se usará para todos los vídeos:
IMAGEN_FIJA = Path(r"D:\AlexPersonal\OPOS25\SETA\audios_m4a\portada.jpg")

# True = genera mp4 con imagen fija (YouTube OK)
# False = genera mp4 solo audio (YouTube normalmente NO)
USAR_IMAGEN = True
# ==========================


def mp3_a_mp4_con_imagen(mp3_path: Path, mp4_path: Path, imagen_path: Path):
    """
    MP4 mínimo para YouTube: imagen fija + audio.
    Vídeo: H.264 muy lento y con bitrate muy bajo (pero suficiente).
    Audio: AAC 64k (mantiene tamaño mínimo).
    """
    cmd = [
        str(FFMPEG),
        "-y",
        "-loop", "1",
        "-i", str(imagen_path),
        "-i", str(mp3_path),

        # vídeo mínimo
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "30",
        "-tune", "stillimage",
        "-pix_fmt", "yuv420p",

        # audio mínimo
        "-c:a", "aac",
        "-b:a", "64k",

        "-shortest",
        str(mp4_path)
    ]
    subprocess.run(cmd, check=True)


def mp3_a_mp4_solo_audio(mp3_path: Path, mp4_path: Path):
    """
    MP4 solo audio (mínimo), pero YouTube normalmente lo rechaza.
    """
    cmd = [
        str(FFMPEG),
        "-y",
        "-i", str(mp3_path),
        "-c:a", "aac",
        "-b:a", "64k",
        str(mp4_path)
    ]
    subprocess.run(cmd, check=True)


def main():
    if not INPUT_DIR.exists():
        print(f"❌ No existe INPUT_DIR: {INPUT_DIR}")
        return

    mp3s = list(INPUT_DIR.glob("*.mp3"))
    if not mp3s:
        print(f"❌ No se han encontrado MP3 en: {INPUT_DIR}")
        return

    if USAR_IMAGEN and not IMAGEN_FIJA.exists():
        print(f"❌ No existe la imagen fija: {IMAGEN_FIJA}")
        return

    print(f"🎵 MP3 encontrados: {len(mp3s)}")
    print(f"📦 Modo: {'con imagen fija' if USAR_IMAGEN else 'solo audio'}")
    print("----")

    for mp3 in mp3s:
        mp4 = OUTPUT_DIR / f"{mp3.stem}.mp4"

        print(f"➡️ Procesando: {mp3.name}")

        try:
            if USAR_IMAGEN:
                mp3_a_mp4_con_imagen(mp3, mp4, IMAGEN_FIJA)
            else:
                mp3_a_mp4_solo_audio(mp3, mp4)

            print(f"   ✅ OK -> {mp4.name}")

        except subprocess.CalledProcessError:
            print(f"   ❌ ERROR convirtiendo {mp3.name}")

    print("----")
    print("✅ Terminado.")


if __name__ == "__main__":
    main()
