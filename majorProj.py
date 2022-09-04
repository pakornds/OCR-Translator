from googletrans import Translator
from tkinter import *
import cv2
import pytesseract as tess
from tkinter import filedialog
import pathlib
import sys


def translator(filename: str) -> str:
    if getattr(sys, 'frozen', False):
        bundle_dir = pathlib.Path(sys._MEIPASS)
    else:
        bundle_dir = pathlib.Path(__file__).parent

    XD = bundle_dir / 'OCR'/'tesseract.exe'
    translator = Translator()
    tess.pytesseract.tesseract_cmd = str(XD)

    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hImg, wImg = gray.shape
    d = tess.image_to_data(gray, output_type=tess.Output.DICT,
                           lang='jpn_vert+jpn+Eng+Tha')

    texts = ''.join(d['text'])
    out = translator.translate(texts, dest="en")

    return texts, out  # merge in tuple


filename = filedialog.askopenfilename(title="Select Image", filetypes=(
    ("jpg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))

texts, out = translator(filename)  # unmerge them
print(texts)
print(out.text)
print()
input("Press enter to proceed...")
