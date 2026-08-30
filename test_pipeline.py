import sys
import re

# 1. Check JD text reaching the route (Simulated)
resume_text = "Python, Flask, REST API, MySQL"
job_description = "Python, Flask, REST API, MySQL, Docker, Kubernetes, React, PostgreSQL, Redis, AWS"

print(f"[DEBUG] JD text received, length={len(job_description)}, first 100 chars: {job_description[:100]!r}")

# Load skills
import pandas as pd
df = pd.read_csv("dataset/skills.csv")
skills_db = {}
for _, row in df.iterrows():
    category = row["category"]
    skill = row["skill"]
    if category not in skills_db:
        skills_db[category] = []
    skills_db[category].append(skill)
print(f"[DEBUG] Loaded {sum(len(v) for v in skills_db.values())} skills from skills.csv")

# 2. Extract skills
def extract_skills(text, skills_db):
    found_skills = []
    categorized_skills = {}
    text = text.lower()
    text = text.replace("/", " ").replace(".", " ").replace("-", " ")
    for category in skills_db:
        categorized_skills[category] = []
    for category, skills in skills_db.items():
        for skill in skills:
            skill_clean = skill.lower()
            skill_clean = skill_clean.replace("/", " ").replace(".", " ").replace("-", " ")
            if re.search(r'\b' + re.escape(skill_clean) + r'\b', text):
                if skill not in found_skills:
                    found_skills.append(skill)
                    categorized_skills[category].append(skill)
    print(f"[DEBUG] Extracted {len(found_skills)} skills from {len(text)} chars of text: {found_skills}")
    return found_skills, categorized_skills

print("\nRunning on Resume:")
resume_skills, _ = extract_skills(resume_text, skills_db)

print("\nRunning on JD:")
jd_skills, _ = extract_skills(job_description, skills_db)

# 4. Matching logic
print(f"[DEBUG] resume_skills={resume_skills}")
print(f"[DEBUG] jd_skills={jd_skills}")

matched_skills = list(set(resume_skills) & set(jd_skills))
missing_skills = list(set(jd_skills) - set(resume_skills))
print(f"[DEBUG] matched={matched_skills}, missing={missing_skills}")

# 5. ATS Score
if len(jd_skills) == 0:
    score = 0
else:
    score = (len(matched_skills) / len(jd_skills)) * 100
print(f"[DEBUG] Score inputs: matched={len(matched_skills)}, jd_skills={len(jd_skills)}, resulting score={score}")
