from services.jd_matcher import compare_resume_with_jd

# CALCULATE ATS SCORE
def calculate_ats_score(resume_text, job_description=None, target_role=None):

    result = compare_resume_with_jd(
        resume_text,
        job_description=job_description,
        target_role=target_role
    )

    matched_skills = result["matched_skills"]
    jd_skills = result["jd_skills"]
    semantic_sim = result.get("semantic_similarity", 0.0)

    if len(jd_skills) == 0:
        skill_score = 0.0
        final_score = semantic_sim
    else:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
        final_score = 0.6 * skill_score + 0.4 * semantic_sim

    # EXPLAINABILITY
    matched_count = len(matched_skills)
    total_count = len(jd_skills)
    is_mapped = result.get("is_mapped_role", True)
    role_display = result.get("target_role_display", target_role or "")

    if is_mapped:
        explanation = (
            f"Score Breakdown: Matched {matched_count}/{total_count} target skills ({round(skill_score, 1)}% skill fit) "
            f"and achieved {semantic_sim}% semantic context similarity with the target position description."
        )
    else:
        explanation = (
            f"Role Note: '{role_display}' evaluated against baseline technical skills: "
            f"Matched {matched_count}/{total_count} baseline skills ({round(skill_score, 1)}% skill fit) "
            f"and achieved {semantic_sim}% semantic context similarity."
        )

    return {
        "ats_score": round(final_score, 2),
        "skill_match_score": round(skill_score, 2),
        "semantic_similarity": semantic_sim,
        "matched_skills": matched_skills,
        "missing_skills": result["missing_skills"],
        "resume_skills": result["resume_skills"],
        "jd_skills": jd_skills,
        "explanation": explanation,
        "is_mapped_role": is_mapped,
        "target_role_display": role_display
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