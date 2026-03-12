import locale
import os
import shutil
import sys
from pdf2image import convert_from_path

def convert_pdfs(lang="en"):
    """
    Convierte todos los archivos PDF en la carpeta de entrada a imágenes,
    mostrando mensajes en el idioma especificado ('en' o 'es').
    """
    # Antes de comenzar, asegurarse de que Poppler esté disponible
    if not ensure_poppler():
        # la función ya imprime un mensaje al usuario; salimos para evitar
        # lanzar excepciones recurrentes más adelante.
        return
    # --- Configuración de idioma ---
    if lang and lang.startswith("es"):
        # Español
        msg_processing = "🔹 Procesando {}..."
        msg_success = "✅ {} convertido correctamente ({} páginas)"
        msg_error = "❌ Error procesando {}: {}"
        msg_completed = "\n🎉 Conversión completada."
        page_name_prefix = "pagina"
        msg_no_pdfs = "🤷 No se encontraron archivos PDF en la carpeta 'pdfs'."
    else:
        # Inglés (por defecto)
        msg_processing = "🔹 Processing {}..."
        msg_success = "✅ {} successfully converted ({} pages)"
        msg_error = "❌ Error processing {}: {}"
        msg_completed = "\n🎉 Conversion completed."
        page_name_prefix = "page"
        msg_no_pdfs = "🤷 No PDF files found in the 'pdfs' folder."

    # --- Configuración de carpetas ---
    input_folder = "pdfs"
    output_folder = "images"
    os.makedirs(output_folder, exist_ok=True)

    # --- Proceso de conversión ---
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(msg_no_pdfs)
        return

    for file in pdf_files:
        pdf_path = os.path.join(input_folder, file)
        pdf_name = os.path.splitext(file)[0]
        pdf_output_dir = os.path.join(output_folder, pdf_name)
        os.makedirs(pdf_output_dir, exist_ok=True)

        print(msg_processing.format(file))

        try:
            pages = convert_from_path(pdf_path, dpi=300)
            for i, page in enumerate(pages):
                image_name = os.path.join(pdf_output_dir, f"{page_name_prefix}_{i + 1}.png")
                page.save(image_name, "PNG")
            print(msg_success.format(file, len(pages)))
        except Exception as e:
            # si el error proviene de la falta de Poppler, ofrecer instrucciones más claras
            err_str = str(e)
            if "poppler" in err_str.lower() or "pdftoppm" in err_str.lower():
                print(msg_error.format(file, e))
                print("⚠️ Parece que Poppler no está instalado o no está en el PATH.\n"
                      "Instala Poppler y asegúrate de que el ejecutable `pdftoppm` sea accesible.\n"
                      "Más información: https://pdf2image.readthedocs.io/en/latest/installation.html")
            else:
                print(msg_error.format(file, e))

    print(msg_completed)

def ensure_poppler():
    """Garantiza que Poppler esté disponible.

    Si ya existe en PATH devuelve True. En Windows intentará
automáticamente descargar y extraer el ZIP del último lanzamiento
oficial junto al ejecutable si no encuentra ninguna instalación.
    """
    # primero, el caso estándar.
    if shutil.which("pdftoppm") or shutil.which("pdftocairo"):
        return True

    # en Windows intentamos descargarlo al mismo directorio que el script
    if os.name == "nt":
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        poppler_dir = os.path.join(base_dir, "poppler")
        
        # buscar Library/bin en la estructura extraída (puede estar en poppler/poppler-*/Library/bin)
        bin_dir = None
        if os.path.isdir(poppler_dir):
            # primero intentar poppler/Library/bin
            candidate = os.path.join(poppler_dir, "Library", "bin")
            if os.path.isdir(candidate) and (shutil.which("pdftoppm", path=candidate) or shutil.which("pdftocairo", path=candidate)):
                bin_dir = candidate
            else:
                # buscar poppler/poppler-*/Library/bin
                for entry in os.listdir(poppler_dir):
                    candidate = os.path.join(poppler_dir, entry, "Library", "bin")
                    if os.path.isdir(candidate) and (shutil.which("pdftoppm", path=candidate) or shutil.which("pdftocairo", path=candidate)):
                        bin_dir = candidate
                        break
        
        if bin_dir:
            # ya descargado anteriormente
            os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
            return True
        
        try:
            url = get_latest_poppler_url()
            print(f"📥 Descargando Poppler desde {url}...")
            download_and_extract(url, poppler_dir)
            
            # buscar el directorio bin en la estructura recién extraída
            bin_dir = None
            candidate = os.path.join(poppler_dir, "Library", "bin")
            if os.path.isdir(candidate):
                bin_dir = candidate
            else:
                # buscar poppler/poppler-*/Library/bin
                for entry in os.listdir(poppler_dir):
                    candidate = os.path.join(poppler_dir, entry, "Library", "bin")
                    if os.path.isdir(candidate):
                        bin_dir = candidate
                        break
            
            if bin_dir and (shutil.which("pdftoppm", path=bin_dir) or shutil.which("pdftocairo", path=bin_dir)):
                os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
                print(f"✅ Poppler instalado localmente en {bin_dir}")
                return True
            else:
                raise RuntimeError(f"No se encontró pdftoppm/pdftocairo en {poppler_dir}")
        except Exception as e:
            print(f"❗ Error al instalar Poppler automáticamente: {e}")
            print("   Por favor instálalo manualmente y asegúrate de que pdftoppm esté en el PATH.")
            return False
    else:
        # no es Windows; solo avisamos
        print("❗ Poppler no detectado: instala Poppler y añade sus binarios al PATH.")
        print("   En Windows puedes descargarlo de https://github.com/oschwartz10612/poppler-windows/releases")
        return False



# helpers para descarga automática en Windows
import json
import zipfile
import urllib.request

def get_latest_poppler_url():
    """Consulta la API de GitHub y devuelve la URL del asset Release-*.zip."""
    api = "https://api.github.com/repos/oschwartz10612/poppler-windows/releases/latest"
    with urllib.request.urlopen(api) as resp:
        data = json.load(resp)
    for asset in data.get("assets", []):
        name = asset.get("name", "")
        if "Release" in name and name.endswith(".zip"):
            return asset.get("browser_download_url")
    raise RuntimeError("No se encontró un asset Release-*.zip en la última release")

def download_and_extract(url, dest):
    """Descarga un ZIP desde `url` y lo extrae en `dest`."""
    os.makedirs(dest, exist_ok=True)
    tmp = os.path.join(dest, "poppler.zip")
    with urllib.request.urlopen(url) as resp, open(tmp, "wb") as out:
        out.write(resp.read())
    with zipfile.ZipFile(tmp, "r") as z:
        z.extractall(dest)
    os.remove(tmp)


if __name__ == "__main__":
    pdf_folder = "pdfs"

    # Determinar idioma sin usar getdefaultlocale (deprecado en 3.15).
    try:
        # establecer la configuración regional al valor por defecto del sistema
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        # si falla, ignorar; simplemente intentaremos obtener la tupla
        pass
    lang_tuple = locale.getlocale()
    lang = lang_tuple[0] if lang_tuple and lang_tuple[0] else "en_US"

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        print(f"📁 Carpeta '{pdf_folder}' creada.")
        print("Por favor, coloca tus archivos PDF en esa carpeta y ejecuta el programa de nuevo.")
        input("\nPresiona ENTER para salir...")
        exit()

    print(f"🌍 Idioma del sistema detectado: {lang}")
    print("▶️ Iniciando conversión...")

    # verificar que Poppler esté accesible antes de iniciar la conversión
    if not ensure_poppler():
        input("\nPresiona ENTER para salir...")
        exit()

    convert_pdfs(lang)
    input("\n✅ Proceso terminado. Presiona ENTER para cerrar...")

