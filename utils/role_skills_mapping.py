# Mapping of common roles to their expected skills

ROLE_SKILLS = {
    "backend developer": ["python", "java", "flask", "django", "node.js", "rest api", "mysql", "postgresql", "mongodb", "redis", "docker", "aws"],
    "frontend developer": ["html", "css", "javascript", "typescript", "react", "angular", "nextjs", "redux", "bootstrap", "tailwind css"],
    "full stack developer": ["html", "css", "javascript", "react", "node.js", "express.js", "rest api", "mysql", "mongodb", "docker", "aws"],
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

def get_skills_for_role(role_name: str) -> list:
    """
    Returns a list of expected skills for the given role name.
    """
    role_clean = role_name.strip().lower()
    return ROLE_SKILLS.get(role_clean, [])
