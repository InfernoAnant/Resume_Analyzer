from services.skill_extractor import extract_skills

# MATCH RESUME VS JD
def compare_resume_with_jd(resume_text, job_description):

    # extract skills from resume
    resume_skills = extract_skills(resume_text)

    # extract skills from JD
    jd_skills = extract_skills(job_description)

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