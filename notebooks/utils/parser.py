import io
import fitz
from PIL import Image
import base64

class Parser:
    """Converts a image file to a base64 string
    @param: str image_path: path to the image file
    @return: list: [base64 string, resolution of the image]
    """
    def imageToBase64(self, image_path):
        img = Image.open(image_path)
        width, height = img.size
        img_base64 = self.__imageToBase64(img)
        return [img_base64, [width, height]]

    """Converts a PDF file to a base64 string
    @param: str pdf_path: path to the PDF file
    @return: list: [base64 string, resolution of the image]
    """
    def pdfToBase64(self, pdf_path, page=0):
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_base64 = self.__imageToBase64(img)
        return [img_base64, [pix.width,pix.height]]

    """Converts a list of text to a list of text prompts
    @param: list of text
    @return: list of text prompts
    """
    def text2prompts(self, list_text):
        return list(map(lambda item: {"type": "text", "text": item}, list_text))

    """Converts a PDF file to a list of image_url prompts
    @param: str pdf_path: path to the PDF file
    @return: list of image_url prompts
    """
    def pdf2prompts(self, pdf_path):
        prompts = []
        while True:
            try:
                page_number = len(prompts)
                base64_page, img_size = self.pdfToBase64(pdf_path, page_number)
                image_url_prompt = {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_page}","detail": "high"}}
                prompts.append(image_url_prompt)
            except Exception:
                break
        return prompts

    def __imageToBase64(self, img):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        return img_base64
