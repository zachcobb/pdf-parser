from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import tempfile
import os
import uvicorn

app = FastAPI()

@app.post("/extract")
async def extract_text(file: UploadFile):
    try:
        # Write file to a temporary location to avoid memory overload
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        full_text = ""
        with fitz.open(tmp_path) as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"

        os.remove(tmp_path)
        return JSONResponse({"text": full_text.strip()})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)

# Add this endpoint to your app.py

@app.post("/extract-raw")
async def extract_text_raw(request: Request):
    try:
        # Read raw body as bytes
        body = await request.body()
        print(f"Raw body length: {len(body)} bytes")
        
        if len(body) == 0:
            return JSONResponse({"error": "No file data received"}, status_code=422)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(body)
            tmp_path = tmp.name
        
        full_text = ""
        with fitz.open(tmp_path) as doc:
            for page in doc:
                full_text += page.get_text("text") + "\n"
        
        os.remove(tmp_path)
        return JSONResponse({"text": full_text.strip()})
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
