# FLASK APP - Run the app using flask --app app.py run
import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
from docx import Document

import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    doc = request.files['document']
    filename = doc.filename
    file_path = os.path.join(UPLOAD_PATH, filename)
    doc.save(file_path)

    file_extension = os.path.splitext(filename)[1].lower()
    data = _read_file_from_path(file_path, file_extension)

    parsed_data = ats_extractor(data)

    return render_template('index.html', data=json.loads(parsed_data))

 
def _read_file_from_path(path, extension):
    """Reads text from the given file based on its extension."""
    data = ""
    if extension == ".pdf":
        reader = PdfReader(path)
        for page in reader.pages:
            data += page.extract_text()
    elif extension == ".docx":
        doc = Document(path)
        for paragraph in doc.paragraphs:
            data += paragraph.text + "\n"
    elif extension == ".txt":
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        raise ValueError("Unsupported file format")

    return data

if __name__ == "__main__":
    #os.makedirs(UPLOAD_PATH, exist_ok=True)
    app.run(debug=True)
