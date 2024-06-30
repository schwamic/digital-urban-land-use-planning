from utils.pdf2base64 import pdf2base64

def pdf2prompts(pdf_path):
    prompts = []
    while True:
        try:
            page_number = len(prompts)
            base64_page=pdf2base64(pdf_path, page_number)
            image_url_prompt = {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_page[0]}","detail": "high"}}
            prompts.append(image_url_prompt)
        except Exception:
            break
    return prompts
