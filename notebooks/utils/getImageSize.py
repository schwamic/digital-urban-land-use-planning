from PIL import Image

"""Returns the size of an imag
@param: str image_path: path to the image file
@return: list: [width, height]
"""
def getImageSize(image_path):
    im = Image.open(image_path)
    width, height = im.size
    return [width, height]
