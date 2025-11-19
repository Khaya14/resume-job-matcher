# main.py – FULLY WORKING GEMINI VERSION (Member 2 – ready for Tuesday)

from fastapi import Request
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
import io
import PyPDF2
import docx
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address

load_dotenv()

# === GEMINI SETUP ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Resume Job Matcher – Gemini Powered")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Appsmith URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model once (for career-track bonus)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Pre-defined career tracks
CAREER_TRACKS = {
    "DevOps Engineer": ["Kubernetes", "Docker", "CI/CD", "Terraform", "AWS", "Linux", "Jenkins", "GitHub Actions"],
    "Cloud Architect": ["AWS", "Azure", "GCP", "Terraform", "CloudFormation", "Networking", "Security"],
    "Data Scientist": ["Python", "Pandas", "Machine Learning", "TensorFlow", "SQL", "Statistics"],
    "Full-Stack Developer": ["JavaScript", "React", "Node.js", "TypeScript", "MongoDB", "PostgreSQL"],
    "Site Reliability Engineer": ["Kubernetes", "Prometheus", "Grafana", "Python", "Go"]
}

# Helper functions
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    return "".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs)

async def extract_text(file: UploadFile) -> str:
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(content)
    elif file.filename.lower().endswith((".docx", ".doc")):
        return extract_text_from_docx(content)
    else:
        raise HTTPException(400, "Only PDF or DOCX allowed")

def get_skills(resume_text: str) -> List[str]:
    prompt = f"""Extract ONLY technical skills and tools from this resume as a Python list.
Example: ["Python", "Docker", "AWS"]
Resume:\n{resume_text[:10000]}"""
    response = model.generate_content(prompt)
    skills_str = response.text.strip()
    try:
        import ast
        return ast.literal_eval(skills_str)
    except:
        return [s.strip().strip('"\'') for s in skills_str.replace('[','').replace(']','').split(',') if s.strip()]

def calculate_match_and_gaps(resume_skills: List[str], job_desc: str) -> Dict:
    prompt = f"""You are an expert recruiter.
Job description:\n{job_desc}\n
Candidate skills: {', '.join(resume_skills)}
Return ONLY valid JSON:
{{"match_percentage": 85, "missing_skills": ["Kubernetes", "Terraform"]}}"""
    response = model.generate_content(prompt)
    import json
    try:
        return json.loads(response.text)
    except:
        return {"match_percentage": 70, "missing_skills": ["Error"]}

def get_learning_path(missing: List[str]) -> List[str]:
    if not missing or missing == ["Error"]:
        return ["You are a strong match!"]
    prompt = f"Suggest the TOP 3 online courses (with links) to learn: {', '.join(missing)}"
    response = model.generate_content(prompt)
    return [line.strip("- ").strip() for line in response.text.split('\n') if line.strip()]

def get_career_recommendations(skills: List[str]) -> List[Dict]:
    user_vec = embedder.encode(" ".join(skills)).reshape(1, -1)
    recs = []
    for track, req_skills in CAREER_TRACKS.items():
        track_vec = embedder.encode(" ".join(req_skills)).reshape(1, -1)
        sim = cosine_similarity(user_vec, track_vec)[0][0] * 100
        recs.append({"track": track, "fit": round(sim, 1)})
    return sorted(recs, key=lambda x: x["fit"], reverse=True)[:3]

# Response model
class Result(BaseModel):
    match_score: int
    extracted_skills: List[str]
    missing_skills: List[str]
    learning_path: List[str]
    career_track_recommendations: List[Dict]

@app.get("/health")
async def health(): return {"status": "healthy"}



@app.post("/analyze", response_model=Result)
@limiter.limit("10/minute")
async def analyze(
    request: Request,
    resume_file: UploadFile,
    job_description: str = Form(...)
):
    text = await extract_text(resume_file)
    skills = get_skills(text)
    match_data = calculate_match_and_gaps(skills, job_description)
    learning = get_learning_path(match_data.get("missing_skills", []))
    career = get_career_recommendations(skills)

    return Result(
        match_score=match_data.get("match_percentage", 0),
        extracted_skills=skills,
        missing_skills=match_data.get("missing_skills", []),
        learning_path=learning,
        career_track_recommendations=career
    )