import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess_text(text):

    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))

    filtered_tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return " ".join(filtered_tokens)

def extract_skills(text, skills_db):

    found_skills = []
    categorized_skills = {}

    # normalize text
    text = text.lower()

    # replace separators for better matching
    text = text.replace("/", " ")

    text = text.replace(".", " ")

    text = text.replace("-", " ")

    # initialize categories dynamically
    for category in skills_db:

        categorized_skills[category] = []

    # scan skills
    for category, skills in skills_db.items():

        for skill in skills:

            skill_clean = skill.lower()

            skill_clean = skill_clean.replace("/", " ")

            skill_clean = skill_clean.replace(".", " ")

            skill_clean = skill_clean.replace("-", " ")

            # better matching
            if skill_clean in text:

                if skill not in found_skills:

                    found_skills.append(skill)
                    categorized_skills[category].append(skill)

    return (
        found_skills,categorized_skills
    )