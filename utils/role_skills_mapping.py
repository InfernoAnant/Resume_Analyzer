# Mapping of common roles to their expected skills

ROLE_SKILLS = {
    "software engineer": ["python", "java", "javascript", "typescript", "react", "node.js", "express.js", "rest api", "postgresql", "docker", "aws", "git", "postman"],
    "backend developer": ["python", "java", "flask", "django", "node.js", "rest api", "mysql", "postgresql", "mongodb", "redis", "docker", "aws"],
    "frontend developer": ["html", "css", "javascript", "typescript", "react", "angular", "nextjs", "redux", "bootstrap", "tailwind css"],
    "full stack developer": ["html", "css", "javascript", "typescript", "react", "node.js", "express.js", "rest api", "postgresql", "mysql", "mongodb", "docker", "aws"],
    "data analyst": ["sql", "power bi", "excel", "tableau", "python", "pandas", "data visualization", "kpi analysis"],
    "data scientist": ["python", "sql", "pandas", "numpy", "statistics", "machine learning", "scikit-learn", "data visualization", "tensorflow"],
    "devops engineer": ["linux", "docker", "kubernetes", "jenkins", "aws", "ansible", "terraform", "github actions", "prometheus"],
    "cloud engineer": ["aws", "azure vm", "google cloud", "docker", "kubernetes", "cloudformation", "vpc", "iam", "linux"],
    "ai engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "computer vision", "llm", "langchain"],
    "machine learning engineer": ["python", "scikit-learn", "tensorflow", "pytorch", "mlflow", "feature engineering", "model deployment", "sql"],
    "mobile developer": ["java", "kotlin", "swift", "flutter", "dart", "firebase", "android studio", "api integration", "cross platform"],
    "qa engineer": ["java", "python", "selenium", "automation testing", "manual testing", "api testing", "postman", "jenkins"],
    "cybersecurity analyst": ["python", "linux", "penetration testing", "ethical hacking", "kali linux", "wireshark", "metasploit", "security auditing"]
}

# Role aliases mapping user/ML input titles to canonical ROLE_SKILLS keys
ROLE_ALIASES = {
    "software engineer": "software engineer",
    "software developer": "software engineer",
    "software dev": "software engineer",
    "swe": "software engineer",
    "sde": "software engineer",
    "full stack engineer": "full stack developer",
    "fullstack engineer": "full stack developer",
    "fullstack developer": "full stack developer",
    "backend engineer": "backend developer",
    "backend dev": "backend developer",
    "frontend engineer": "frontend developer",
    "frontend dev": "frontend developer",
    "web developer": "full stack developer",
    "web engineer": "full stack developer",
    "devops": "devops engineer",
    "sre": "devops engineer",
    "site reliability engineer": "devops engineer",
    "ml engineer": "machine learning engineer",
    "ai/ml engineer": "ai engineer",
    "ai developer": "ai engineer",
    "data engineer": "data scientist",
    "qa": "qa engineer",
    "security analyst": "cybersecurity analyst",
    "cybersecurity": "cybersecurity analyst"
}

def resolve_role_name(role_name: str) -> tuple[str, list, bool]:
    """
    Resolves a input role name string to (canonical_role_name, skills_list, is_mapped).
    """
    if not role_name or not role_name.strip():
        return ("", [], False)

    role_clean = role_name.strip().lower()

    # 1. Exact match in ROLE_SKILLS
    if role_clean in ROLE_SKILLS:
        return (role_clean.title(), ROLE_SKILLS[role_clean], True)

    # 2. Alias match
    if role_clean in ROLE_ALIASES:
        canonical = ROLE_ALIASES[role_clean]
        return (canonical.title(), ROLE_SKILLS[canonical], True)

    # 3. Substring / Fuzzy match against canonical keys
    for key in ROLE_SKILLS:
        if key in role_clean or role_clean in key:
            return (key.title(), ROLE_SKILLS[key], True)

    # 4. Keyword fuzzy checks
    if "software" in role_clean or "developer" in role_clean or "engineer" in role_clean:
        return ("Software Engineer", ROLE_SKILLS["software engineer"], True)
    if "data" in role_clean:
        return ("Data Analyst", ROLE_SKILLS["data analyst"], True)
    if "cloud" in role_clean or "aws" in role_clean:
        return ("Cloud Engineer", ROLE_SKILLS["cloud engineer"], True)
    if "ai" in role_clean or "ml" in role_clean:
        return ("AI Engineer", ROLE_SKILLS["ai engineer"], True)

    # If completely unmapped, return original title with empty list and is_mapped=False
    return (role_name.strip().title(), [], False)

def get_skills_for_role(role_name: str) -> list:
    """
    Returns a list of expected skills for the given role name.
    Preserves backward compatibility while resolving aliases and fuzzy matches.
    """
    _, skills, _ = resolve_role_name(role_name)
    return skills
