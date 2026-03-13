from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import shutil
import os
from nlp_utils import extract_text_from_pdf, extract_text_from_docx, calculate_ats_score, analyze_resume_text

app = FastAPI(title="Resume Analyzer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_role: str = Form(""),
    target_companies: str = Form("")
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = ""
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_location)
    elif file.filename.lower().endswith(".docx"):
        text = extract_text_from_docx(file_location)
    else:
        try:
            with open(file_location, "r", encoding="utf-8") as f:
                text = f.read()
        except:
             with open(file_location, "r", encoding="latin-1") as f:
                text = f.read()

    if not text:
        return {
             "filename": file.filename,
             "error": "Could not extract text"
        }

    score, score_breakdown = calculate_ats_score(text)
    analysis = analyze_resume_text(text)
    
    # Calculate Company Matches (Simulated Logic)
    company_matches = []
    if target_companies:
        companies = [c.strip() for c in target_companies.split(',') if c.strip()]
        for company in companies:
            # Simple simulation: Random variation around the base ATS score
            # In a real app, this would match against specific company job descriptions
            import random
            match_score = min(98, max(40, score + random.randint(-15, 10)))
            
            # Custom feedback based on score
            status = "Highly Eligible" if match_score >= 75 else "Needs Improvement"
            missing = []
            if match_score < 75:
                missing = ["Cloud Skills", "System Design"] if "Engineer" in job_role else ["Data Analysis", "SQL"]
                
            company_matches.append({
                "company": company,
                "match_score": match_score,
                "status": status,
                "missing_skills": missing
            })

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "ats_score": score,
        "score_breakdown": score_breakdown,
        "summary": "Resume content extracted successfully.",
        "text_preview": text[:500],
        "strengths": ["Clear formatting" if score > 50 else "Needs improvement"],
        "weaknesses": ["Low keyword density" if score < 50 else "Good keyword usage"],
        "details": analysis,
        "job_role": job_role,
        "company_matches": company_matches
    }

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

@app.post("/chat")
async def chat_resume(request: ChatRequest):
    # Simple rule-based logic for demo
    msg = request.message.lower()
    response = "I'm here to help improve your resume. Ask me about your score or specific sections."
    
    if "keyword" in msg or "missing" in msg:
        response = "Based on your resume, you might want to add keywords like 'Docker', 'Kubernetes' if you are targeting DevOps roles, or 'React', 'Next.js' for Frontend."
    elif "experience" in msg or "work" in msg:
        response = "Your experience section is good, but could use more quantifiable metrics. For example, instead of 'Improved performance', try 'Improved page load time by 40%'."
    elif "score" in msg:
        response = "Your ATS score is calculated based on keyword density, formatting, and completeness. Improving your summary section is the easiest way to boost it."
    elif "summary" in msg:
        response = "Your summary should be a 2-3 sentence elevator pitch. Focus on your years of experience and top 3 technical skills."
        
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
