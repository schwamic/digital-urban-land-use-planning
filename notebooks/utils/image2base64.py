import base64

"""Converts a PDF file to a base64 string
@param: str image_path: path to the image file
@return: base64 string
"""
def image2base64(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
