import json
import uuid
import sys
import os
import re
import datetime


def load_and_merge_json_arrays(json_path):
    """
    Carga uno o varios arrays JSON consecutivos y los fusiona en un único array.
    """
    with open(json_path, "r", encoding="utf-8-sig") as f:
        raw_content = f.read()

    if not raw_content.strip():
        raise ValueError("El archivo JSON está vacío.")

    decoder = json.JSONDecoder()
    index = 0
    merged = []
    parsed_values = 0

    while index < len(raw_content):
        while index < len(raw_content) and raw_content[index].isspace():
            index += 1

        if index >= len(raw_content):
            break

        try:
            value, next_index = decoder.raw_decode(raw_content, index)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido cerca de la posición {exc.pos}: {exc.msg}") from exc

        if not isinstance(value, list):
            raise ValueError("Cada bloque JSON de nivel superior debe ser un array.")

        merged.extend(value)
        parsed_values += 1
        index = next_index

    if parsed_values == 0:
        raise ValueError("No se encontró ningún array JSON válido.")

    return merged, parsed_values

def compress_answer_options(json_str):
    """
    Comprime cada elemento del array answerOptions en una sola línea
    """
    # Patrón para encontrar el array answerOptions completo
    pattern = r'"answerOptions":\s*\[(.*?)\]'
    
    def compress_options(match):
        options_content = match.group(1)
        # Encontrar cada objeto individual {...}
        obj_pattern = r'\{[^{}]*\}'
        objects = re.findall(obj_pattern, options_content, re.DOTALL)
        
        compressed_objects = []
        for obj in objects:
            # Eliminar saltos de línea y espacios extra
            compressed = re.sub(r'\s+', ' ', obj)
            compressed = re.sub(r'\s*([{}:,])\s*', r'\1', compressed)
            compressed_objects.append(compressed)
        
        # Reconstruir el array con cada objeto en una línea
        result = '"answerOptions": [\n'
        for i, obj in enumerate(compressed_objects):
            comma = ',' if i < len(compressed_objects) - 1 else ''
            result += f'     {obj}{comma}\n'
        result += '    ]'
        return result
    
    return re.sub(pattern, compress_options, json_str, flags=re.DOTALL)

def update_guids(json_path, backup=True):
    # Comprobar que el archivo existe
    if not os.path.exists(json_path):
        print(f"❌ No se encontró el archivo: {json_path}")
        return

    # Leer y fusionar arrays JSON consecutivos si existen
    try:
        data, block_count = load_and_merge_json_arrays(json_path)
    except ValueError as exc:
        print(f"❌ {exc}")
        return

    if block_count > 1:
        print(f"🔧 Se han fusionado {block_count} arrays JSON en un único array ({len(data)} elementos).")

    # Crear copia de seguridad con timestamp
    if backup:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{json_path}.{timestamp}.bak"
        os.rename(json_path, backup_path)
        print(f"📦 Copia de seguridad creada: {backup_path}")

    # Actualizar los GUID
    for obj in data:
        obj["guid"] = str(uuid.uuid4())

    # Serializar a JSON con formato normal
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    
    # Comprimir los answerOptions
    json_str = compress_answer_options(json_str)

    # Guardar el JSON actualizado
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_str)

    print(f"✅ GUIDs actualizados y answerOptions comprimidos en {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python update_guids.py ruta/al/archivo.json")
    else:
        update_guids(sys.argv[1])
