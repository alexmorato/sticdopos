import os
import json
import sys
import subprocess
from datetime import datetime, timezone


# CONFIGURACIÓN
# Lista de palabras prohibidas
palabras_prohibidas = ["manifest"]  # Modifica según necesidad


def normalizar_nombre_archivo(nombre):
    """
    Normaliza el nombre de archivo según las reglas:
    - Espacios se reemplazan por "_"
    - Caracteres con acentos u otros diacríticos se reemplazan por "x"
    - Si empieza por 't' minúscula, se cambia por 'T' mayúscula
    """
    # Separar nombre y extensión
    nombre_base, extension = os.path.splitext(nombre)
    
    # 1. Reemplazar espacios por "_"
    nombre_base = nombre_base.replace(" ", "_")
    
    # 2. Reemplazar caracteres con acentos o no ASCII por "x"
    nombre_normalizado = ""
    for char in nombre_base:
        # Verificar si el carácter es ASCII básico (sin acentos)
        if ord(char) < 128 and (char.isalnum() or char in ['_', '-', '.']):
            nombre_normalizado += char
        else:
            # Reemplazar caracteres raros por "x"
            nombre_normalizado += "x"
    
    # 3. Si empieza por 't' minúscula, cambiarla por 'T' mayúscula
    if nombre_normalizado and nombre_normalizado[0] == 't':
        nombre_normalizado = 'T' + nombre_normalizado[1:]
    
    # Reconstruir con la extensión
    return nombre_normalizado + extension


def obtener_fecha_commit(raiz_git, ruta_relativa):
    resultado = subprocess.run(
        ["git", "-C", raiz_git, "log", "-1", "--format=%ct", "--", ruta_relativa],
        check=True,
        capture_output=True,
        text=True
    )
    timestamp = resultado.stdout.strip()
    if not timestamp:
        return None

    return datetime.fromtimestamp(int(timestamp), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Leer carpeta desde parámetros
if len(sys.argv) != 2:
    print("Uso: python generate_manifest.py <ruta_carpeta>")
    sys.exit(1)

carpeta = sys.argv[1]
carpeta_destino = carpeta  # Carpeta y destino son iguales

if not os.path.isdir(carpeta):
    print(f"Error: La carpeta '{carpeta}' no existe")
    sys.exit(1)

try:
    resultado_git = subprocess.run(
        ["git", "-C", os.path.abspath(carpeta), "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True
    )
    raiz_git = resultado_git.stdout.strip()
except (OSError, subprocess.CalledProcessError):
    print(f"Error: La carpeta '{carpeta}' no pertenece a un repositorio Git")
    sys.exit(1)

# PASO 1: Renombrar archivos que necesiten normalización
print("=" * 60)
print("PASO 1: Normalizando nombres de archivos...")
print("=" * 60)

archivos_renombrados = 0
for f in os.listdir(carpeta):
    ruta_completa = os.path.join(carpeta, f)
    if os.path.isfile(ruta_completa):
        nombre_normalizado = normalizar_nombre_archivo(f)
        
        if nombre_normalizado != f:
            ruta_nueva = os.path.join(carpeta, nombre_normalizado)
            
            # Verificar que no exista ya un archivo con el nuevo nombre
            if os.path.exists(ruta_nueva):
                print(f"  ⚠️  ADVERTENCIA: '{nombre_normalizado}' ya existe. Saltando '{f}'")
                continue
            
            try:
                os.rename(ruta_completa, ruta_nueva)
                print(f"  ✓ Renombrado: '{f}' → '{nombre_normalizado}'")
                archivos_renombrados += 1
            except Exception as e:
                print(f"  ✗ Error al renombrar '{f}': {e}")

print(f"\nArchivos renombrados: {archivos_renombrados}")
print()

# PASO 2: Generar manifest con los nombres ya normalizados
print("=" * 60)
print("PASO 2: Generando manifest...")
print("=" * 60)

# Listar solo archivos (no carpetas) y filtrar por palabras prohibidas
ficheros = []
for f in os.listdir(carpeta):
    if os.path.isfile(os.path.join(carpeta, f)):
        if not any(palabra in f for palabra in palabras_prohibidas):
            ficheros.append(f)

# Mantener un orden estable en manifest.json sin alterar el orden de entrada
# que utiliza manifest_date.json para resolver fechas iguales.
ficheros_ordenados = sorted(ficheros)

# Crear el diccionario con el formato requerido
manifest = {
    "files": ficheros_ordenados
}


# Guardar el manifest en un archivo JSON en la carpeta destino
manifest_path = os.path.join(carpeta_destino, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# PASO 3: Generar manifest_date.json con fechas de actualización
print("\nPASO 3: Generando manifest_date.json...")
manifest_date_list = []
archivos_sin_commit = []
fecha_actual = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for fname in ficheros:
    ruta = os.path.relpath(os.path.join(os.path.abspath(carpeta), fname), raiz_git)
    updated_str = obtener_fecha_commit(raiz_git, ruta)
    if updated_str is None:
        archivos_sin_commit.append(fname)
        updated_str = fecha_actual
    manifest_date_list.append({"file": fname, "updated": updated_str})

# Fechas descendentes, con orden estable por nombre para fechas iguales.
manifest_date_list.sort(key=lambda item: item["file"])
manifest_date_list.sort(
    key=lambda item: item["updated"],
    reverse=True
)

if archivos_sin_commit:
    print(
        f"Aviso: {len(archivos_sin_commit)} archivo(s) sin commit; "
        "se usa la fecha actual UTC."
    )

manifest_date = {"files": manifest_date_list}
manifest_date_path = os.path.join(carpeta_destino, "manifest_date.json")
with open(manifest_date_path, "w", encoding="utf-8") as f:
    json.dump(manifest_date, f, ensure_ascii=False, indent=2)

print(f"\n✓ Manifest_date generado correctamente en: {manifest_date_path}")
print(f"  Total de archivos en manifest_date: {len(manifest_date_list)}")
print("=" * 60)