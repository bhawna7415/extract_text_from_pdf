import os
import io
from flask import Flask, request, render_template, redirect, url_for, send_file,make_response
import fitz  
import pytesseract
from PIL import Image


project_root = os.path.dirname(os.path.realpath('__file__'))
static_path = os.path.join(project_root, 'app/static')
app = Flask(__name__, template_folder= 'templates')
context_set = ""

# @app.route('/')
# def hello_world():
#     return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    success_message = None

    if request.method == 'POST':
        pdf_file = request.files['pdfFile']
        if pdf_file:
            pdf_bytes = pdf_file.read()
            extracted_text = extract_text_from_pdf(pdf_bytes)

            extracted_text_file = io.BytesIO()
            extracted_text_file.write(extracted_text.encode('utf-8'))
            extracted_text_file.seek(0)

            success_message = "Text extracted successfully!"

            response = make_response(send_file(
                extracted_text_file,
                as_attachment=True,
                download_name='textfile.txt',
                mimetype='text/plain'
            ))
            return response

    return render_template('index.html', success_message=success_message)

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_bytes):
    images = []
    pdf_document = fitz.open("pdf_file.pdf", pdf_bytes)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()
        img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
        images.append(img)
    pdf_document.close()

    extracted_text = ""
    for image in images:
        text = extract_text_from_image(image)
        extracted_text += text

    return extracted_text

if __name__ == '__main__':
    app.run(debug=True)