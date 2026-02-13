# AI Research Portal
# Live Deployment

 # Frontend
https://research-platform-mauve.vercel.app/

# Backend API
https://research-platform-0s31.onrender.com

# Backend API Documentation
https://research-platform-0s31.onrender.com/docs



# Overview

AI Research Portal is a structured research tool built for analysts.
This system is not an open-ended chatbot. Instead, it processes uploaded documents and produces structured, research-ready outputs.

The current implementation supports Earnings Call and Management Commentary analysis.

Users can upload a document and receive structured insights including tone, confidence level, key positives, key concerns, forward guidance, and growth initiatives.

The system is designed to be reliable, structured, and analyst-friendly.

# Note
Backend is hosted on Render free tier. The service may take 30 to 60 seconds to wake up after inactivity.

# Features

# Document Upload
Supports PDF and TXT files.

Structured Earnings Analysis
Detects whether document is a valid earnings transcript.
If not, returns structured unsupported document response.

# Management Tone Detection
Optimistic
Cautious
Neutral
Pessimistic

Confidence Level Classification
High
Medium
Low

Key Positives Extraction
Extracts 3 to 5 major strengths or performance highlights.

Key Concerns Extraction
Extracts 3 to 5 risks or challenges.

Forward Guidance Extraction
Revenue outlook
Margin outlook
Capex outlook

Capacity Utilization Detection

Growth Initiatives Identification

Analyst Export
Download structured analysis in JSON format.

Multi Document Support
Users can analyze multiple documents sequentially.

File Size Protection
Maximum file size is limited to 5MB to prevent memory overload.

Automatic File Cleanup
Uploaded files are removed after processing to prevent storage accumulation.

Architecture

Frontend
React.js deployed on Vercel.

Backend
FastAPI deployed on Render.

AI Model
Google Gemini API via google genai SDK.

# System Flow

User uploads document in frontend.
Frontend sends file to backend API.
Backend validates file type and size.
Backend extracts text from document.
LLM processes text and generates structured JSON output.
Frontend renders structured analyst view.
User can export results.

# Tech Stack

# Frontend
React.js
JavaScript
Axios

# Backend
FastAPI
Uvicorn
Pydantic
Google GenAI SDK
PDFPlumber

# Deployment
Render for backend
Vercel for frontend

# Project Structure

research_platform__

# backend
main.py
llm.py
parser.py
models.py
requirements.txt

# frontend
package.json
src
public

# README.md

# API Endpoints

GET /

Returns health check message.

POST /analyze

Accepts file upload.
Processes document.
Returns structured earnings analysis.

# Document Validation Logic

If document does not contain earnings related content, system returns

document_type Unsupported
confidence_level Low
confidence_reasoning Explanation of why document is unsupported

This prevents hallucination and ensures research reliability.

# Confidence Logic

Confidence level is determined based on language certainty and presence of structured financial guidance.

High
Clear numerical guidance and strong declarative language.

Medium
Mixed signals or partially specified guidance.

Low
Vague statements or missing financial indicators.

# Limitations

Backend runs on free Render tier.
Cold start delay may occur after inactivity.

Maximum file size is 5MB.

Currently supports PDF and TXT files.

Docx support removed to reduce memory usage and improve stability.

# How to Run Locally

# Backend

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend

cd frontend
npm install
npm start

# Environment Variables

Backend requires the following environment variable

GEMINI_API_KEY

In Render dashboard, add this under Environment Variables.

Do not commit .env file to repository.

Assignment Completion Scope

This implementation satisfies:

Document upload
Document ingestion
End to end research tool processing
Structured research output
Deployment with public access
Working API keys
Clear usability
Analyst ready structured format

Quality and structure of output are prioritized over raw performance.

# Future Improvements

Add CSV export option
Add Financial Statement Extraction tool
Add Authentication layer
Add Document history storage
Add Dashboard analytics

# Author

Shrinath Patil
Software Developer
