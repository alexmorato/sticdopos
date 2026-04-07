import os
import sys
import datetime

# Uso: python add_9h_to_mtime.py <carpeta>
def add_9h_to_files(folder):
    for root, _, files in os.walk(folder):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                # Obtener mtime actual
                mtime = os.path.getmtime(fpath)
                # Sumar 9 horas
                new_mtime = mtime + 9 * 3600
                # Actualizar mtime
                os.utime(fpath, (os.path.getatime(fpath), new_mtime))
                print(f"Actualizado: {fpath}")
            except Exception as e:
                print(f"Error en {fpath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python add_9h_to_mtime.py <carpeta>")
        sys.exit(1)
    carpeta = sys.argv[1]
    if not os.path.isdir(carpeta):
        print(f"No existe la carpeta: {carpeta}")
        sys.exit(1)
    add_9h_to_files(carpeta)
