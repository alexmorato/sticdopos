import os

# Nombres requeridos
NOMBRES = ["alex", "elena", "tania", "sergio"]

# Carpeta base
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "apunts_new")

# Solo carpetas TXX
carpetas_txx = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and d.startswith("T") and d[1:].isdigit()]

faltantes_global = {}

for carpeta in sorted(carpetas_txx):
    path_tema = os.path.join(BASE_DIR, carpeta)
    encontrados = {nombre: {"jpg": False, "dir": False} for nombre in NOMBRES}

    # Buscar .jpg en la carpeta principal
    archivos = os.listdir(path_tema)
    for nombre in NOMBRES:
        for f in archivos:
            if f.lower().endswith(".jpg") and nombre in f.lower():
                encontrados[nombre]["jpg"] = True
            if os.path.isdir(os.path.join(path_tema, f)) and nombre in f.lower():
                encontrados[nombre]["dir"] = True

    # Buscar .jpg dentro de subcarpetas con nombre
    for nombre in NOMBRES:
        subdir = os.path.join(path_tema, nombre)
        if os.path.isdir(subdir):
            for f in os.listdir(subdir):
                if f.lower().endswith(".jpg"):
                    encontrados[nombre]["jpg"] = True

    # Reportar faltantes
    faltantes = []
    for nombre in NOMBRES:
        if not encontrados[nombre]["jpg"]:
            faltantes.append(f".jpg {nombre}")
        if not encontrados[nombre]["dir"]:
            faltantes.append(f".pdf {nombre}")
    if faltantes:
        faltantes_global[carpeta] = faltantes

if not faltantes_global:
    print("Todo OK: Todos los nombres y carpetas requeridos encontrados en cada TXX.")
else:
    print("Faltan archivos/carpetas en las siguientes carpetas:")
    for carpeta, faltantes in faltantes_global.items():
        print(f"{carpeta}: {', '.join(faltantes)}")
