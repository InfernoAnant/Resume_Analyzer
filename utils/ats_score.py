def calculate_ats_score(found_skills,resume_text):

    found_skills = list(set(found_skills))
    skill_count = len(found_skills)
    score = 0

    # Skill Score (Max 40)
    score += min(skill_count * 2,40)

    # Important Skills Bonus (Max 25)
    important_skills = [
        "python",
        "sql",
        "machine learning",
        "flask",
        "django",
        "react",
        "tensorflow",
        "opencv",
        "github",
        "docker",
        "aws"
    ]

    important_count = 0

    for skill in important_skills:

        if skill.lower() in [
            s.lower()
            for s in found_skills
        ]:

            important_count += 1

    score += min(
        important_count * 3,
        25
    )

    # Category Diversity Bonus (Max 20)
    categories = {

        "Programming": [
            "python",
            "java",
            "c",
            "c++",
            "javascript"
        ],

        "Web Development": [
            "html",
            "css",
            "flask",
            "django",
            "react"
        ],

        "Database": [
            "sql",
            "mysql",
            "mongodb"
        ],

        "AI/ML": [
            "machine learning",
            "tensorflow",
            "opencv",
            "nlp"
        ],

        "Cloud": [
            "aws",
            "azure"
        ],

        "Data Analysis": [
            "pandas",
            "numpy",
            "matplotlib"
        ]
    }
    category_count = 0

    for category, skills in categories.items():

        for skill in skills:

            if skill.lower() in [
                s.lower()
                for s in found_skills
            ]:

                category_count += 1
                break

    score += min(
        category_count * 3,
        20
    )

    # Resume Section Bonus
    text = resume_text.lower()

    if "project" in text:
        score += 5

    if "education" in text:
        score += 3

    if "certification" in text:
        score += 3

    if "experience" in text:
        score += 4

    # Portfolio Bonus
    if "github" in text:
        score += 3

    if "linkedin" in text:
        score += 2

    # Resume Strength Bonus
    if skill_count >= 15:
        score += 10

    elif skill_count >= 10:
        score += 5

    # Final Adjustments
    if score > 95:
        score = 95

    if score < 15 and skill_count > 0:
        score = 15

    return round(score)