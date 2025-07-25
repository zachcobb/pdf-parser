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

