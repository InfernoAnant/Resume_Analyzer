import pandas as pd

# LOAD SKILLS DATABASE
skills_df = pd.read_csv("dataset/skills.csv")

# convert all skills to lowercase
SKILLS = skills_df["skill"].str.lower().tolist()

# EXTRACT SKILLS FUNCTION
def extract_skills(text):

    # convert text to lowercase
    text = text.lower()

    found_skills = []

    # check every skill
    for skill in SKILLS:

        if skill in text:

            found_skills.append(skill)

    # remove duplicates
    return list(set(found_skills))

# TEST
if __name__ == "__main__":

    sample = """

    Developed backend APIs using Python Flask.

    Worked with SQL database.

    Used Docker deployment.

    Integrated AWS cloud services.

    """

    skills = extract_skills(sample)

    print("Detected skills:")

    print(skills)