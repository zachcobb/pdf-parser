# app.py
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import base64

app = FastAPI()

@app.post("/extract")
async def extract_text(file: UploadFile):
    data = await file.read()
    doc = fitz.open(stream=data, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"
    return JSONResponse({"text": full_text})
