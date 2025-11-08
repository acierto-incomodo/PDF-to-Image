import os
from pdf2image import convert_from_path

# Carpeta donde están tus PDFs
input_folder = "pdfs"
output_folder = "images"

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Buscar todos los PDFs en la carpeta
for file in os.listdir(input_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, file)
        pdf_name = os.path.splitext(file)[0]
        pdf_output_dir = os.path.join(output_folder, pdf_name)

        # Crear carpeta con el nombre del PDF
        os.makedirs(pdf_output_dir, exist_ok=True)

        print(f"🔹 Procesando {file}...")

        try:
            pages = convert_from_path(pdf_path, dpi=300)
            for i, page in enumerate(pages):
                image_name = os.path.join(pdf_output_dir, f"pagina_{i + 1}.png")
                page.save(image_name, "PNG")
            print(f"✅ {file} convertido correctamente ({len(pages)} páginas)")
        except Exception as e:
            print(f"❌ Error procesando {file}: {e}")

print("\n🎉 Conversión completada.")
