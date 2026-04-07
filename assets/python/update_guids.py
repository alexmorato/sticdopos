import json
import uuid
import sys
import os
import re

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

    # Leer el JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("❌ El JSON debe ser un array de objetos.")
        return

    # Crear copia de seguridad con timestamp
    if backup:
        import datetime
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
