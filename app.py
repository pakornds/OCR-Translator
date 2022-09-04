import tempfile
from googletrans import Translator
import cv2
import pytesseract as tess
import pathlib
import sys
from flask import Flask, render_template, request, redirect, url_for, Response
import os
from os.path import splitext

UPLOAD_FOLDER = "C:\Vscode\majorProj\temp"
app = Flask(__name__)


def translator(path: str) -> str:
    if getattr(sys, 'frozen', False):
        bundle_dir = pathlib.Path(sys._MEIPASS)
    else:
        bundle_dir = pathlib.Path(__file__).parent

    XD = bundle_dir / 'OCR'/'tesseract.exe'
    tess.pytesseract.tesseract_cmd = str(XD)

    translator = Translator()
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hImg, wImg = gray.shape

    result = tess.image_to_data(gray, output_type=tess.Output.DICT,
                                lang='jpn_vert+jpn+Eng+Tha')
    texts = ''.join(result['text'])
    out = translator.translate(texts, dest="en")
    return texts, out.text


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/uploader", methods=['POST'])
def upload_file():
    result = ""
    if request.method == 'POST':
        print("Form Data Received!!")
        if "file" not in request.files:
            print("field not exist")
            return redirect(url_for('home'))

        uploadedImg = request.files['file']
        print(uploadedImg)
        if uploadedImg.filename == "":
            print("empty file name")
            return redirect(url_for('home'))

        img_name, img_ext = splitext(uploadedImg.filename)

        image_handle, image_path = tempfile.mkstemp(
            prefix=img_name, suffix=img_ext)
        os.close(image_handle)
        uploadedImg.save(image_path)

        try:
            result = translator(image_path)
            return render_template('result.html', result=result)
        except Exception as e:
            return Response('Error {e}', status=500)
        finally:
            os.unlink(image_path)
