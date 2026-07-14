import pandas as pd

from utils.pdf_reader import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.ats_score import calculate_ats_score
from utils.role_predictor import predict_role
from utils.ai_feedback import get_ai_feedback


def load_skills():

    df = pd.read_csv("dataset/skills.csv")

    skills_db = {}

    for _, row in df.iterrows():

        category = row["category"]
        skill = row["skill"]

        if category not in skills_db:

            skills_db[category] = []

        skills_db[category].append(skill)

    return skills_db


def analyze_resume(filepath):

    skills_db = load_skills()

    # EXTRACT PDF TEXT
    text = extract_text_from_pdf(filepath)

    # SKILL EXTRACTION
    found_skills, categorized_skills = extract_skills(text, skills_db)

    # ATS SCORE
    ats_score = calculate_ats_score(found_skills, text)

    # ML PREDICTION
    predictions = predict_role(text)
    predicted_role = predictions[0]["role"]

    # SUGGESTIONS
    suggestions = []

    if len(
        categorized_skills.get(
            "Programming",[]
        )
    ) < 2:

        suggestions.append(
            "Add more programming skills."
        )

    if len(
        categorized_skills.get(
            "Web Development",
            []
        )
    ) == 0:

        suggestions.append(
            "Mention web development technologies."
        )

    if len(
        categorized_skills.get(
            "AI/ML",
            []
        )
    ) == 0:

        suggestions.append(
            "Add AI/ML related projects."
        )

    if "github" not in found_skills:

        suggestions.append(
            "Add GitHub profile."
        )

    if ats_score < 40:

        suggestions.append(
            "Resume ATS score is low."
        )

    if len(
        suggestions
    ) == 0:

        suggestions.append(
            "Excellent resume! Your profile looks strong."
        )

    # AI FEEDBACK
    if ats_score < 60:

        ai_feedback = get_ai_feedback(
            found_skills,
            ats_score,
            predicted_role
        )

    else:

        ai_feedback = """
Excellent resume profile.

Your resume already contains strong technical skills and ATS-friendly keywords.

Suggestions:
- Add measurable achievements
- Include GitHub portfolio links
- Add internship experience
"""

    # RETURN RESULT
    return {

        # NEW (for ATS + JD matching)
        "raw_text": text,

        "skills": found_skills,

        "categorized_skills": categorized_skills,

        "score": ats_score,

        "role": predicted_role,

        "top_predictions": predictions,

        "suggestions": suggestions,

        "ai_feedback": ai_feedback
    }
