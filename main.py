import pytesseract
from PIL import Image
from pdf2image import convert_from_path

path = "" #path to a pdf file

images = convert_from_path(path, 500, poppler_path='poppler-23.11.0/Library/bin/')

pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR/tesseract.exe"
print(pytesseract.image_to_string(images[0], lang='eng+rus'))
