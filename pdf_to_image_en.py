import os
from pdf2image import convert_from_path

# Folder where your PDFs are located
input_folder = "pdfs"
output_folder = "images"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Search all PDFs in the folder
for file in os.listdir(input_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, file)
        pdf_name = os.path.splitext(file)[0]
        pdf_output_dir = os.path.join(output_folder, pdf_name)

        # Create folder with the same name as the PDF
        os.makedirs(pdf_output_dir, exist_ok=True)

        print(f"🔹 Processing {file}...")

        try:
            pages = convert_from_path(pdf_path, dpi=300)
            for i, page in enumerate(pages):
                image_name = os.path.join(pdf_output_dir, f"page_{i + 1}.png")
                page.save(image_name, "PNG")
            print(f"✅ {file} successfully converted ({len(pages)} pages)")
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

print("\n🎉 Conversion completed.")
