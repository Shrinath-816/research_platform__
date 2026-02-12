from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from parser import extract_text
from llm import analyze_earnings_call

app = FastAPI(title="Research Portal API")

# -------------------------
# CORS (Important for frontend later)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Upload Directory Setup
# -------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 5


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

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    return {
        "filename": file.filename,
        "text_preview": text[:1000]
    }


# -------------------------
# Analyze Endpoint
# -------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    validate_file(file)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text(file_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text.")

    # Run LLM analysis
    result = analyze_earnings_call(text)

    return {
    "filename": file.filename,
    "analysis": result
}

