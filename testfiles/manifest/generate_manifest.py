import os
import argparse
import json
import subprocess
from datetime import datetime, timezone


# CONFIGURACIÓN
# Lista de palabras prohibidas
palabras_prohibidas = ["manifest"]  # Modifica según necesidad
# Fecha ISO 8601 a partir de la cual se mantienen las fechas existentes.
# Puede sobrescribirse con --fecha-limite.
FECHA_LIMITE_ACTUALIZACION = "2026-11-22T00:00:00Z"


def parsear_fecha(valor):
    valor_normalizado = valor.strip()
    if valor_normalizado.endswith("Z"):
        valor_normalizado = valor_normalizado[:-1] + "+00:00"

    try:
        fecha = datetime.fromisoformat(valor_normalizado)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"fecha inválida '{valor}'; usa un formato ISO 8601 como 2026-01-01 "
            "o 2026-01-01T00:00:00Z"
        ) from exc

    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)

    return fecha.astimezone(timezone.utc)


def cargar_fechas_existentes(manifest_date_path):
    try:
        with open(manifest_date_path, "r", encoding="utf-8") as f:
            contenido = json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"El archivo '{manifest_date_path}' no contiene JSON válido: {exc}"
        ) from exc

    ficheros = contenido.get("files")
    if not isinstance(ficheros, list):
        raise ValueError(
            f"El archivo '{manifest_date_path}' no tiene una lista 'files' válida"
        )

    fechas_existentes = {}
    for entrada in ficheros:
        if not isinstance(entrada, dict):
            raise ValueError(
                f"Entrada inválida en '{manifest_date_path}': se esperaba un objeto"
            )

        nombre = entrada.get("file")
        fecha = entrada.get("updated")
        if not isinstance(nombre, str) or not isinstance(fecha, str):
            raise ValueError(
                f"Entrada inválida en '{manifest_date_path}': "
                "se requieren 'file' y 'updated' como textos"
            )
        fechas_existentes[nombre] = fecha

    return fechas_existentes


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
parser = argparse.ArgumentParser(
    description="Genera manifest.json y manifest_date.json para una carpeta."
)
parser.add_argument("ruta_carpeta", help="Carpeta cuyos archivos se incluirán")
parser.add_argument(
    "--fecha-limite",
    type=parsear_fecha,
    default=(
        parsear_fecha(FECHA_LIMITE_ACTUALIZACION)
        if FECHA_LIMITE_ACTUALIZACION
        else None
    ),
    help=(
        "Fecha ISO 8601 del corte. Las fechas del manifest anteriores a este "
        "momento se conservarán sin consultar Git."
    ),
)
args = parser.parse_args()

carpeta = args.ruta_carpeta
fecha_limite = args.fecha_limite
carpeta_destino = carpeta  # Carpeta y destino son iguales

if not os.path.isdir(carpeta):
    print(f"Error: La carpeta '{carpeta}' no existe")
    parser.exit(1)

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
    parser.exit(1)

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
archivos_con_fecha_conservada = []
fecha_actual = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
manifest_date_path = os.path.join(carpeta_destino, "manifest_date.json")
try:
    fechas_existentes = cargar_fechas_existentes(manifest_date_path)
except ValueError as exc:
    parser.error(str(exc))

for fname in ficheros:
    updated_existente = fechas_existentes.get(fname)
    if updated_existente is not None and fecha_limite is not None:
        try:
            fecha_existente = parsear_fecha(updated_existente)
        except argparse.ArgumentTypeError as exc:
            parser.error(
                f"La fecha existente de '{fname}' en '{manifest_date_path}' "
                f"no es válida: {exc}"
            )

        if fecha_existente < fecha_limite:
            manifest_date_list.append(
                {"file": fname, "updated": updated_existente}
            )
            archivos_con_fecha_conservada.append(fname)
            continue

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
if archivos_con_fecha_conservada:
    print(
        f"Se conservaron {len(archivos_con_fecha_conservada)} fecha(s) "
        "anteriores al límite sin consultar Git."
    )

manifest_date = {"files": manifest_date_list}
with open(manifest_date_path, "w", encoding="utf-8") as f:
    json.dump(manifest_date, f, ensure_ascii=False, indent=2)

print(f"\n✓ Manifest_date generado correctamente en: {manifest_date_path}")
print(f"  Total de archivos en manifest_date: {len(manifest_date_list)}")
print("=" * 60)