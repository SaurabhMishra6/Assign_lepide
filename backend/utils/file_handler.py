import os
from fastapi import UploadFile

UPLOAD_DIR = "static/uploads"

def save_file(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location