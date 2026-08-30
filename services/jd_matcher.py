from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.skill_extractor import extract_skills
from services.resume_service import load_skills

def calculate_semantic_similarity(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0
    try:
        vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        matrix = vec.fit_transform([resume_text, job_description])
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0

# MATCH RESUME VS JD
def compare_resume_with_jd(resume_text, job_description=None, target_role=None):
    
    skills_db = load_skills()

    # extract skills from resume
    resume_skills, _ = extract_skills(resume_text, skills_db)

    # get skills for JD or Role
    jd_skills = []
    semantic_similarity = 0.0
    is_mapped_role = True
    role_display_name = target_role or ""

    if target_role and target_role.strip():
        from utils.role_skills_mapping import resolve_role_name
        role_display_name, jd_skills, is_mapped_role = resolve_role_name(target_role)

        # Fallback if target role skills baseline could not be mapped
        if not jd_skills:
            from utils.role_predictor import predict_role
            fallback_predictions = predict_role(resume_text)
            fallback_role = fallback_predictions[0]["role"] if fallback_predictions else "Software Engineer"
            _, jd_skills, _ = resolve_role_name(fallback_role)
            is_mapped_role = False

        # Construct synthetic role text for semantic similarity
        role_text = f"Seeking candidate experienced in {', '.join(jd_skills)} for {role_display_name} position."
        semantic_similarity = calculate_semantic_similarity(resume_text, role_text or target_role)
    elif job_description and job_description.strip():
        jd_skills, _ = extract_skills(job_description, skills_db)
        semantic_similarity = calculate_semantic_similarity(resume_text, job_description)

    # Synonym-aware matched and missing skills calculation
    from utils.skill_extractor import SYNONYM_MAP

    def normalize_skill(s):
        s_clean = s.strip().lower()
        return SYNONYM_MAP.get(s_clean, s_clean)

    resume_skills_map = {normalize_skill(s): s for s in resume_skills}
    jd_skills_map = {normalize_skill(s): s for s in jd_skills}

    matched_keys = set(resume_skills_map.keys()) & set(jd_skills_map.keys())
    matched_skills = [jd_skills_map[k] for k in matched_keys]

    missing_keys = set(jd_skills_map.keys()) - set(resume_skills_map.keys())
    missing_skills = [jd_skills_map[k] for k in missing_keys]

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "semantic_similarity": round(semantic_similarity * 100, 2),
        "is_mapped_role": is_mapped_role,
        "target_role_display": role_display_name
    }

# TEST
if __name__ == "__main__":

    resume = """

    Developed backend APIs using Python Flask.

    Worked with SQL database.

    Used Docker deployment.

    """

    job_description = """

    Looking for developer with Python Flask SQL AWS Docker Kubernetes Redis

    """

    result = compare_resume_with_jd(

        resume,
        job_description
    )

    print("\nResume Skills:", result["resume_skills"])

    print("\nJD Skills:", result["jd_skills"])

    print("\nMatched Skills:", result["matched_skills"])

    print("\nMissing Skills:", result["missing_skills"])