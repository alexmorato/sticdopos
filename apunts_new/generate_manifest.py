import os
import json

# =========================
# CONFIGURACIÓN
# =========================
BASE_DIR = "apunts_new"          # Carpeta base a escanear
OUTPUT_FILE = "apunts_new/manifest.json"

MD_EXT = ".md"
IMG_EXT = ".jpg"
URL_MANIFEST = "manifest_url.json"

# =========================
# FUNCIONES AUXILIARES
# =========================
def is_file_with_ext(path, ext):
    return os.path.isfile(path) and path.lower().endswith(ext)

def list_files_with_ext(folder, ext):
    return sorted(
        f for f in os.listdir(folder)
        if is_file_with_ext(os.path.join(folder, f), ext)
    )

# =========================
# LÓGICA PRINCIPAL
# =========================
def generate_manifest(base_dir):
    # 1. Ruta absoluta a partir de la relativa
    abs_path = os.path.abspath(base_dir)

    # 2. Última carpeta de la ruta
    base_folder = os.path.basename(os.path.normpath(abs_path))

    manifest = {
        "base": base_folder,
        "temes": {}
    }

    if not os.path.isdir(base_dir):
        raise RuntimeError(f"La carpeta base no existe: {base_dir}")

    for tema in sorted(os.listdir(base_dir)):
        tema_path = os.path.join(base_dir, tema)

        if not os.path.isdir(tema_path):
            continue  # Ignorar ficheros sueltos en base

        tema_data = {}

        # ---- MD en root ----
        md_files = list_files_with_ext(tema_path, MD_EXT)
        if md_files:
            tema_data["md"] = md_files

        # ---- JPG en root (infografías) ----
        img_files = list_files_with_ext(tema_path, IMG_EXT)
        if img_files:
            tema_data["info"] = img_files

        # ---- URLs desde manifest_url.json ----
        url_manifest_path = os.path.join(tema_path, URL_MANIFEST)
        if os.path.isfile(url_manifest_path):
            try:
                with open(url_manifest_path, "r", encoding="utf-8") as url_file:
                    urls_data = json.load(url_file)
                    if urls_data and isinstance(urls_data, list):
                        tema_data["urls"] = urls_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Advertencia: Error leyendo {url_manifest_path}: {e}")

        # ---- Subcarpetas de slides ----
        slides = []

        for item in sorted(os.listdir(tema_path)):
            item_path = os.path.join(tema_path, item)

            if not os.path.isdir(item_path):
                continue

            imgs = list_files_with_ext(item_path, IMG_EXT)
            if imgs:
                slides.append({
                    "dir": item,
                    "imgs": imgs
                })

        if slides:
            tema_data["slides"] = slides

        # Solo añadir el tema si tiene contenido relevante
        if tema_data:
            manifest["temes"][tema] = tema_data

    return manifest

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    manifest = generate_manifest(BASE_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Manifest generado correctamente: {OUTPUT_FILE}")
