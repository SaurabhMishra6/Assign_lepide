𝗙𝘂𝗿𝘁𝗵𝗲𝗿 𝗿𝗲𝗮𝗱𝗶𝗻𝗴 𝗮𝗻𝗱 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻:
React useState hook: https://react.dev/reference/react/use...
create-react-app: https://create-react-app.dev/docs/get...
FastAPI Request Files: https://fastapi.tiangolo.com/tutorial...
FastAPI and CORS: https://fastapi.tiangolo.com/tutorial...
FormData: https://fastapi.tiangolo.com/tutorial...
FormData (JavaScript.info): https://javascript.info/formdata


Google, ChatGPT, stackoverflow, etc





#Backend
Install Required Packages:
pip install fastapi[all]  # If using FastAPI
pip install flask  # If using Flask
pip install pydantic  # For data validation (needed for FastAPI)
pip install torch transformers  # For using a pre-trained language model
pip install python-multipart  # To handle file uploads

 * ->> Implement File Handling and Storage:
Create file_handler.py inside the utils/ directory:

import os
from fastapi import UploadFile

UPLOAD_DIR = "static/uploads"

def save_file(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location




-------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------

  * ->> Set Up the LLM (Language Model):
Create summarize_model.py inside the models/ directory:

from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']




------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------


* ->>Create the Backend API:
Create app.py:

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


--------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
    

#Frontend

* ->>Implement File Upload Component:
Create FileUpload.js in components/:

import React, { useState } from "react";
import axios from "../services/api";

function FileUpload({ setSummary }) {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post("/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });

        const summarizeResponse = await axios.post("/summarize", formData);
        setSummary(summarizeResponse.data.summary);
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload and Summarize</button>
        </div>
    );
}

export default FileUpload;

----------------------------------------------------------------------
-------------------------------------------------------------------


Implement API Service:
Create api.js in services/:


import axios from "axios";

export default axios.create({
    baseURL: "http://localhost:8000",
});


----------------------------------------------------------------------------------
----------------------------------------------------------------------------


Display Summarized Text:
Create SummaryDisplay.js in components/:

import React from "react";

function SummaryDisplay({ summary }) {
    return (
        <div>
            <h2>Summary</h2>
            <p>{summary}</p>
        </div>
    );
}

export default SummaryDisplay;


------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------

Integrate Components in App.js:


import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import SummaryDisplay from "./components/SummaryDisplay";

function App() {
    const [summary, setSummary] = useState("");

    return (
        <div>
            <h1>Document Summarizer</h1>
            <FileUpload setSummary={setSummary} />
            {summary && <SummaryDisplay summary={summary} />}
        </div>
    );
}

export default App;
