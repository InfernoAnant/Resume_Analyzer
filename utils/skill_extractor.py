import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

SYNONYM_MAP = {
    "express": "express.js",
    "expressjs": "express.js",
    "postgres": "postgresql",
    "k8s": "kubernetes",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "nodejs": "node.js",
    "node": "node.js",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "aws cloud": "aws",
    "amazon web services": "aws",
    "gcp": "google cloud platform",
    "azure cloud": "azure",
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
}

def preprocess_text(text):

    text = text.lower()
    try:
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [
            word for word in tokens
            if word not in stop_words
        ]
        return " ".join(filtered_tokens)
    except Exception:
        return text

def extract_skills(text, skills_db):

    found_skills = []
    categorized_skills = {}

    # normalize text
    text_lower = text.lower()
    
    # Expand synonyms in text
    expanded_text = text_lower
    for alias, canonical in SYNONYM_MAP.items():
        expanded_text = re.sub(r'\b' + re.escape(alias) + r'\b', f"{alias} {canonical}", expanded_text)

    # replace separators for matching
    clean_text_content = expanded_text.replace("/", " ").replace(".", " ").replace("-", " ")

    # initialize categories dynamically
    for category in skills_db:
        categorized_skills[category] = []

    # scan skills
    for category, skills in skills_db.items():

        for skill in skills:

            skill_clean = skill.lower().replace("/", " ").replace(".", " ").replace("-", " ")

            # Check boundary match in expanded text or cleaned text
            if re.search(r'\b' + re.escape(skill_clean) + r'\b', clean_text_content) or \
               re.search(r'\b' + re.escape(skill.lower()) + r'\b', expanded_text):

                if skill not in found_skills:
                    found_skills.append(skill)
                    categorized_skills[category].append(skill)

    return (
        found_skills, categorized_skills
    )