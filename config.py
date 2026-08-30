import os

UPLOAD_FOLDER = os.path.abspath("storage/uploads")

REPORT_FOLDER = "static/reports"

DATABASE = "resume.db"

SKILLS_CSV = "dataset/skills.csv"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Feature Flag: Toggle Recruiter Batch Mode UI (Set True to enable batch upload tab)
SHOW_RECRUITER_BATCH = False