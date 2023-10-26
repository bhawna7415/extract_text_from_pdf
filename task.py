import fitz  
import pytesseract
from PIL import Image

pdf_file_path = "Germany.pdf"

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()
        img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
        images.append(img)
    pdf_document.close()
    return images

images = extract_images_from_pdf(pdf_file_path)

extracted_text = ""
for image in images:
    text = extract_text_from_image(image)
    extracted_text += text

print(extracted_text)

with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(extracted_text)
