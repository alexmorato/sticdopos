import os
import sys
import fitz  # PyMuPDF
from PIL import Image

def pdf_to_jpg_in_folder(pdf_path, dpi=150):
    """Convierte un PDF a imágenes JPG en una carpeta con el nombre del PDF"""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"No existe el fichero: {pdf_path}")

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("El fichero no es un PDF")

    # Obtener el directorio padre y el nombre del archivo sin extensión
    parent_folder = os.path.dirname(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Crear carpeta con el nombre del PDF
    output_folder = os.path.join(parent_folder, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    # Abrir el PDF
    pdf_document = fitz.open(pdf_path)
    
    # Calcular zoom para el DPI deseado (72 es el DPI por defecto)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    
    # Convertir cada página a imagen
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap(matrix=mat)
        
        page_str = f"{page_num + 1:02d}"
        output_path = os.path.join(output_folder, f"img_{page_str}.jpg")
        pix.save(output_path, "jpeg", jpg_quality=75)
    
    pdf_document.close()

    # Borrar el PDF original
    os.remove(pdf_path)
    print(f"✓ PDF '{pdf_name}' convertido a {len(pdf_document)} imágenes en carpeta '{pdf_name}'")


def png_to_jpg_optimized(png_path, target_size_kb=450):
    """Convierte un PNG a JPG optimizado (alrededor de 400-500KB)"""
    if not os.path.isfile(png_path):
        raise FileNotFoundError(f"No existe el fichero: {png_path}")

    if not png_path.lower().endswith(".png"):
        raise ValueError("El fichero no es un PNG")

    # Abrir la imagen PNG
    img = Image.open(png_path)
    
    # Convertir a RGB si es necesario (los PNG pueden tener canal alpha)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background

    # Crear el nombre del archivo JPG
    jpg_path = os.path.splitext(png_path)[0] + ".jpg"
    
    # Intentar encontrar la calidad óptima para el tamaño deseado
    quality = 85
    img.save(jpg_path, "JPEG", quality=quality, optimize=True)
    
    # Ajustar calidad si es necesario
    file_size_kb = os.path.getsize(jpg_path) / 1024
    
    # Si el archivo es muy grande, reducir calidad
    if file_size_kb > target_size_kb * 1.2:  # 20% de margen
        quality = 75
        img.save(jpg_path, "JPEG", quality=quality, optimize=True)
        file_size_kb = os.path.getsize(jpg_path) / 1024
    
    # Si aún es muy grande, reducir más
    if file_size_kb > target_size_kb * 1.5:
        quality = 65
        img.save(jpg_path, "JPEG", quality=quality, optimize=True)
        file_size_kb = os.path.getsize(jpg_path) / 1024
    
    # Borrar el PNG original
    os.remove(png_path)
    print(f"✓ PNG '{os.path.basename(png_path)}' convertido a JPG ({file_size_kb:.0f}KB)")


def process_folder(folder_path):
    """Procesa todos los PDFs y PNGs en una carpeta y sus subcarpetas recursivamente"""
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"No existe la carpeta: {folder_path}")

    # Buscar todos los archivos PDF y PNG recursivamente
    pdfs = []
    pngs = []
    
    print(f"🔍 Buscando PDFs y PNGs en '{folder_path}' y subcarpetas...")
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(".pdf"):
                pdfs.append(file_path)
            elif file.lower().endswith(".png"):
                pngs.append(file_path)
    
    # Procesar PDFs
    print(f"\n📄 Encontrados {len(pdfs)} PDFs para procesar...")
    for pdf_path in pdfs:
        try:
            pdf_to_jpg_in_folder(pdf_path)
        except Exception as e:
            print(f"✗ Error procesando {os.path.basename(pdf_path)}: {e}")
    
    # Procesar PNGs
    print(f"\n🖼️  Encontrados {len(pngs)} PNGs para convertir...")
    for png_path in pngs:
        try:
            png_to_jpg_optimized(png_path)
        except Exception as e:
            print(f"✗ Error procesando {os.path.basename(png_path)}: {e}")
    
    print(f"\n✅ Proceso completado: {len(pdfs)} PDFs y {len(pngs)} PNGs procesados")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python pdf_to_jpg.py <ruta_carpeta>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)
