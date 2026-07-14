from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# cache for repeated requests
feedback_cache = {}

def get_ai_feedback(skills, score, role):

    feedback = []

    #LOCAL FALLBACK
    if score < 30:
        feedback.append(
            "• Improve ATS score by adding more technical keywords."
        )

    if "sql" not in [s.lower() for s in skills]:
        feedback.append(
            "• Add SQL and database-related experience."
        )

    if "github" not in [s.lower() for s in skills]:
        feedback.append(
            "• Include GitHub profile and projects."
        )

    if "machine learning" not in [s.lower() for s in skills]:
        feedback.append(
            "• Add AI/ML related projects."
        )

    #QUICK LOCAL FEEDBACK
    quick_feedback = {

        "AI Engineer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build TensorFlow and PyTorch projects
• Add model deployment experience
• Improve deep learning portfolio

Missing Skills:
• Computer Vision
• NLP
• MLOps

Career Advice:
• Build production AI projects
• Learn model optimization
• Focus on real world datasets
""",

        "Machine Learning Engineer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build end to end ML pipeline projects
• Improve model evaluation knowledge
• Add predictive modeling projects

Missing Skills:
• Feature Engineering
• MLflow
• Hyperparameter Tuning

Career Advice:
• Learn production ML systems
• Practice advanced model training
• Focus on deployment pipelines
""",

        "Data Scientist": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Add data science case studies
• Improve statistical modeling knowledge
• Build predictive analytics projects

Missing Skills:
• Advanced Statistics
• Feature Engineering
• Model Interpretation

Career Advice:
• Work on real datasets
• Improve analytical thinking
• Build portfolio with research projects
""",

        "Data Analyst": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Add dashboard based projects
• Improve SQL query skills
• Work on business analytics projects

Missing Skills:
• Power BI
• Tableau
• Advanced SQL

Career Advice:
• Build analytics dashboards
• Learn business reporting
• Improve visualization skills
""",

        "Backend Developer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Add Flask/Django production projects
• Improve REST API development skills
• Add backend deployment experience

Missing Skills:
• Redis
• Docker
• PostgreSQL

Career Advice:
• Build scalable backend systems
• Learn microservices architecture
• Deploy live backend applications
""",

        "Frontend Developer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build modern React projects
• Improve responsive UI design
• Learn frontend optimization techniques

Missing Skills:
• TypeScript
• Next.js
• Redux

Career Advice:
• Build portfolio websites
• Focus on UI/UX improvement
• Learn advanced frontend frameworks
""",

        "Full Stack Developer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build full stack deployed projects
• Improve API integration skills
• Add authentication based projects

Missing Skills:
• Node.js
• MongoDB
• Docker

Career Advice:
• Build end to end applications
• Learn system design
• Deploy full stack apps online
""",

        "DevOps Engineer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Practice CI/CD pipeline creation
• Improve infrastructure automation skills
• Build cloud deployment projects

Missing Skills:
• Terraform
• Kubernetes
• Jenkins

Career Advice:
• Learn cloud architecture
• Automate deployment pipelines
• Build scalable infrastructure
""",

        "Cloud Engineer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build AWS/Azure deployment projects
• Learn cloud security concepts
• Practice infrastructure management

Missing Skills:
• AWS Lambda
• VPC
• CloudFormation

Career Advice:
• Get cloud certifications
• Learn distributed systems
• Build production cloud solutions
""",

        "Cybersecurity Analyst": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Practice penetration testing projects
• Improve vulnerability assessment skills
• Learn security monitoring tools

Missing Skills:
• SIEM Tools
• Network Monitoring
• Security Auditing

Career Advice:
• Practice ethical hacking labs
• Learn advanced network security
• Participate in security competitions
""",

        "Mobile Developer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build production mobile apps
• Improve app performance optimization
• Add cross platform app projects

Missing Skills:
• Firebase
• API Integration
• State Management

Career Advice:
• Build Play Store apps
• Learn app architecture patterns
• Focus on mobile UI design
""",

        "QA Engineer": """
Smart Resume Analysis

Resume Improvement Suggestions:
• Build automation testing projects
• Improve test case writing skills
• Practice API testing workflows

Missing Skills:
• Selenium
• Postman
• JUnit

Career Advice:
• Learn automated testing frameworks
• Practice software quality assurance processes
• Build real-world testing projects
"""
    }

    #SKIP API FOR STRONG RESUME
    if score >= 55:

        return """
Smart Resume Analysis

Resume Improvement Suggestions:
• Resume ATS score is already strong
• Add measurable project achievements
• Add internship experience

Missing Skills:
• Improve technical specialization
• Add advanced real-world projects
• Improve portfolio quality

Career Advice:
• Build production-level projects
• Focus on one specialization
• Keep GitHub portfolio updated
"""

    #USE LOCAL QUICK FEEDBACK
    if score > 35 and role in quick_feedback:
        return quick_feedback[role]

    #CACHE CHECK
    cache_key = f"{role}_{score//10}"

    if cache_key in feedback_cache:
        return feedback_cache[cache_key]

    #GEMINI API CALL
    try:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("API key missing")

        prompt = f"""
Resume review.

Role: {role}
Skills: {', '.join(skills[:8])}
ATS Score: {score}

Give:
3 resume improvements
3 missing skills
3 career suggestions

Under 120 words.
Simple bullet points only.
No markdown.
"""

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if (
            hasattr(response, "text")
            and response.text
            and response.text.strip()
        ):

            text = response.text.strip()
            text = text.replace("###", "")
            text = text.replace("**", "")
            text = text.replace("* ", "• ")

            feedback_cache[cache_key] = text

            return text

        raise Exception("Empty Gemini response")

    except Exception as e:
        print("Gemini Error:", str(e))

        return f"""
AI Generated Feedback Unavailable (Using Smart Local Analysis)

Resume Improvement Suggestions:
{chr(10).join(feedback[:3])}

Missing Skills:
• Add industry relevant technical skills
• Add more project-based experience
• Improve resume keyword optimization

Career Advice:
• Build more real-world projects
• Keep resume ATS optimized
• Add certifications and internship experience
"""