import io
import fitz
from PIL import Image
import base64

"""Converts a PDF file to a base64 string
@param: str pdf_path: path to the PDF file
@return: base64 string
"""
def pdf2base64(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
    return img_base64
