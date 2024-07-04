from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import base64

"""Adds axis to the image and returns the base64 encoded image
@param: str image_path: path to the image file
@return: str: base64 encoded image
"""
def imageWithAxis2Base64(image_path):
    img = np.asarray(Image.open(image_path))
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.imshow(img)
    plt.savefig("./cache/plot.png", dpi=300)
    cached_img_path = "./cache/plot.png"
    with open(cached_img_path, "rb") as image_file:
        cached_img_b64 = base64.b64encode(image_file.read()).decode('utf-8')
    os.remove("./cache/plot.png")
    return cached_img_b64
