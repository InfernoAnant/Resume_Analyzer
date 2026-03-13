import spacy
import re
from pdfminer.high_level import extract_text
import docx
import os

# Load model roughly
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None # Handle case where it's not downloaded yet

def extract_text_from_pdf(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return ""

def calculate_ats_score(text):
    if not text:
        return 0, {}
        
    score = 0
    breakdown = {}
    
    # 1. Section Headers (simplified) - 30 points
    sections = ["experience", "education", "skills", "projects", "summary", "contact"]
    found_sections = [k for k in sections if k.lower() in text.lower()]
    section_score = (len(found_sections) / len(sections)) * 30
    score += section_score
    breakdown["sections"] = int((len(found_sections) / len(sections)) * 100)

    # 2. Length check (approx 400-2000 words is good) - 10 points
    word_count = len(text.split())
    if 400 <= word_count <= 2000:
        score += 10
        breakdown["length"] = 100
    elif word_count > 100:
        score += 5
        breakdown["length"] = 50
    else:
        breakdown["length"] = 20

    # 3. Action verbs - 20 points
    action_verbs = ["led", "developed", "managed", "created", "designed", "implemented", "optimized", "achieved", "improved"]
    verb_count = sum(1 for word in text.lower().split() if word in action_verbs)
    if verb_count > 10:
        score += 20
        breakdown["verbs"] = 100
    elif verb_count > 5:
        score += 10
        breakdown["verbs"] = 50
    else:
        breakdown["verbs"] = 20
    
    # 4. Contact info check - 20 points
    contact_score = 0
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        contact_score += 10
    if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text): 
        contact_score += 10
    score += contact_score
    breakdown["contact"] = int((contact_score / 20) * 100)
        
    # 5. File format/readability (implied by successful extraction) - 20 pts
    score += 20
    breakdown["formatting"] = 100

    return min(100, int(score)), breakdown

def analyze_resume_text(text):
    if not nlp:
        return {"error": "Model not loaded"}
        
    doc = nlp(text)
    
    # Extract entities
    skills = []
    # Common tech keywords to look for explicitly (since mild NLP might miss them)
    tech_keywords = ["python", "java", "script", "react", "node", "aws", "docker", "sql", "git", "linux", "agile", "scrum", "cloud", "api", "rest", "json", "html", "css", "machine learning", "ai"]
    
    text_lower = text.lower()
    for kw in tech_keywords:
        if kw in text_lower:
            skills.append(kw.capitalize())

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "LANGUAGE"]: 
             skills.append(ent.text)
             
    # Deduplicate
    skills = list(set(skills))
    
    # Extract email and phone for display
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    return {
        "text_length": len(text),
        "word_count": len(text.split()),
        "sentences": len(list(doc.sents)),
        "extracted_skills": skills[:15], # Top 15
        "contact_info": {
            "email": email.group(0) if email else "Not found",
            "phone": phone.group(0) if phone else "Not found"
        }
    }
