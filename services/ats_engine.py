from services.jd_matcher import compare_resume_with_jd

# CALCULATE ATS SCORE
def calculate_ats_score(resume_text, job_description):

    result = compare_resume_with_jd(
        resume_text,
        job_description
    )

    matched_skills = result[
        "matched_skills"
    ]

    jd_skills = result[
        "jd_skills"
    ]

    # avoid division by zero
    if len(jd_skills) == 0:

        score = 0

    else:

        score = (len(matched_skills) / len(jd_skills)) * 100


    return {

        "ats_score": round(score, 2),

        "matched_skills":

            matched_skills,

        "missing_skills":

            result["missing_skills"],

        "resume_skills":

            result["resume_skills"],

        "jd_skills":

            jd_skills
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

    result = calculate_ats_score(
        resume,
        job_description
    )

    print("\nATS Score:", result["ats_score"], "%")

    print("\nMatched Skills:", result["matched_skills"])

    print("\nMissing Skills:", result["missing_skills"])