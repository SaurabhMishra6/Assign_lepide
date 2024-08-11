from fastapi import FastAPI, File, UploadFile
from utils.file_handler import save_file
from models.summarize_model import summarize_text

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile):
    file_location = save_file(file)
    return {"file_location": file_location}

@app.post("/summarize")
async def summarize(file: UploadFile):
    file_location = save_file(file)
    with open(file_location, "r") as f:
        text = f.read()
    summary = summarize_text(text)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)