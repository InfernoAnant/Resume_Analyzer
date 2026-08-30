from utils.skill_extractor import extract_skills
from services.resume_service import load_skills

# MATCH RESUME VS JD
def compare_resume_with_jd(resume_text, job_description=None, target_role=None):
    
    skills_db = load_skills()

    # extract skills from resume
    resume_skills, _ = extract_skills(resume_text, skills_db)

    # get skills for JD or Role
    jd_skills = []
    if target_role:
        from utils.role_skills_mapping import get_skills_for_role
        jd_skills = get_skills_for_role(target_role)
    elif job_description and job_description.strip():
        jd_skills, _ = extract_skills(job_description, skills_db)

    # matched skills
    matched_skills = list(
        set(resume_skills) & set(jd_skills)
    )

    # missing skills
    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    return {

        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
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