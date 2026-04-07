import os
import json
import argparse
from datetime import datetime


# =====================================================
# CONFIGURACIÓN
# =====================================================

# Ficheros que NO se deben incluir en el JSON (nombre exacto)
FICHEROS_DESCARTADOS = [
    "manifest.json",
    "manifest_v2.json",
    "README.md"
]

# Valores por defecto si no se pasan parámetros
DIRECTORIO_POR_DEFECTO = "../../testfiles"
FICHERO_DESTINO_POR_DEFECTO = "../../testfiles/manifest_v2.json"


def generar_json_carpeta(directorio_origen, fichero_destino):
    if not os.path.isdir(directorio_origen):
        raise ValueError(f"La ruta no es un directorio válido: {directorio_origen}")

    ficheros_info = []

    for nombre_fichero in os.listdir(directorio_origen):

        # Omitir ficheros descartados
        if nombre_fichero in FICHEROS_DESCARTADOS:
            continue

        ruta_fichero = os.path.join(directorio_origen, nombre_fichero)
        ruta_fichero = ruta_fichero.replace("\\", "/")

        if os.path.isfile(ruta_fichero):
            timestamp = os.path.getmtime(ruta_fichero)
            fecha_modificacion = datetime.fromtimestamp(timestamp).isoformat()

            ficheros_info.append({
                "nombre": nombre_fichero,
                "ruta": ruta_fichero,
                "fecha_modificacion": fecha_modificacion
            })

    resultado = {
        "directorio": directorio_origen,
        "total_ficheros": len(ficheros_info),
        "ficheros": ficheros_info
    }

    with open(fichero_destino, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genera un JSON con los ficheros de un directorio y su fecha de modificación"
    )

    parser.add_argument("--origen", help="Ruta del directorio a analizar")
    parser.add_argument("--destino", help="Ruta del fichero JSON de salida")

    args = parser.parse_args()

    directorio = args.origen or DIRECTORIO_POR_DEFECTO
    destino = args.destino or FICHERO_DESTINO_POR_DEFECTO

    generar_json_carpeta(directorio, destino)
    print(f"JSON generado correctamente en: {destino}")
