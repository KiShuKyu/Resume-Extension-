import pdfplumber
from PIL import Image
import pytesseract

def extract_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    if len(text.strip()) < 50:
        text = ocr_pdf(file)

    return text


def ocr_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            image = page.to_image(resolution=200).original
            text += pytesseract.image_to_string(image)

    return text

