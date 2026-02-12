from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from parser import extract_text
from llm import analyze_earnings_call

app = FastAPI(title="Research Portal API")

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in real production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Config
# -------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# -------------------------
# Helper Function
# -------------------------
def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    return ext


# -------------------------
# Upload Endpoint
# -------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    validate_file(file)

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size {MAX_FILE_SIZE_MB}MB."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        text = extract_text(file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text.")

        return {
            "filename": file.filename,
            "text_preview": text[:1000]
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# -------------------------
# Analyze Endpoint
# -------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    validate_file(file)

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size {MAX_FILE_SIZE_MB}MB."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        text = extract_text(file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text.")

        result = analyze_earnings_call(text)

        return {
            "filename": file.filename,
            "analysis": result
        }

    finally:
        # Clean up to prevent storage/memory growth
        if os.path.exists(file_path):
            os.remove(file_path)
