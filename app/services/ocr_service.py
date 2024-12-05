# import pytesseract
from PIL import Image

def perform_ocr(image_file):
    img = Image.open(image_file)
    # text = pytesseract.image_to_string(img)
    return img
