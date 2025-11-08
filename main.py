import locale
import subprocess
import os

# Nombre de la carpeta donde estarán los PDFs
pdf_folder = "pdfs"

# Verificar si la carpeta existe
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)
    print(f"📁 Created folder '{pdf_folder}'.")
    print("Please place your PDF files in that folder and run the program again.")
    input("\nPress ENTER to exit...")
    exit()

# Detectar idioma del sistema
lang = locale.getdefaultlocale()[0]
print(f"🌍 Detected system language: {lang}")

# Escoger el script según idioma
if lang and lang.startswith("es"):
    script = "pdf_to_images_es.py"
else:
    script = "pdf_to_images_en.py"

# Comprobar que el script exista
if not os.path.exists(script):
    print(f"❌ No se encontró el archivo '{script}'. Asegúrate de que esté en la misma carpeta que este main.py.")
else:
    print(f"▶️ Ejecutando {script}...")
    subprocess.run(["python", script])

input("\n✅ Proceso terminado. Presiona ENTER para cerrar...")
