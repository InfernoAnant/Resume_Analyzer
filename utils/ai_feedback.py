from google import genai
from dotenv import load_dotenv
import os
from cachetools import TTLCache
from utils.logger import logger

load_dotenv()

# Bounded TTL Cache for AI feedback (1000 items max, 1 hour TTL)
feedback_cache = TTLCache(maxsize=1000, ttl=3600)

import re

def get_ai_feedback(skills, score, role, raw_text=""):

    skills_lower = [s.lower() for s in skills]
    cache_key = f"{role}_{','.join(sorted(skills_lower))}_{round(score)}"

    if cache_key in feedback_cache:
        return feedback_cache[cache_key]

    # Detect projects in raw_text if present
    project_matches = re.findall(r'(?:project|platform|app|system|build)[:\s\n–-]+([A-Z][A-Za-z0-9\s–-]+)', raw_text, re.IGNORECASE)
    detected_projects = [p.strip() for p in project_matches if len(p.strip()) > 3 and len(p.strip()) < 30][:2]

    has_github = "github" in skills_lower or bool(re.search(r'github\.com|\bgithub\b', raw_text, re.IGNORECASE))
    has_git = "git" in skills_lower or bool(re.search(r'\bgit\b', raw_text, re.IGNORECASE))
    has_docker = "docker" in skills_lower or bool(re.search(r'\bdocker\b', raw_text, re.IGNORECASE))
    has_aws = "aws" in skills_lower or bool(re.search(r'\baws\b', raw_text, re.IGNORECASE))

    # DYNAMIC GROUNDED LOCAL FALLBACK
    dynamic_suggestions = []
    if skills:
        top_skills_str = ", ".join([s.title() for s in skills[:5]])
        dynamic_suggestions.append(f"- Strong foundation in {top_skills_str}. Expand metric-driven impact bullet points.")
    if detected_projects:
        dynamic_suggestions.append(f"- Highlight technical architecture details for key projects ({', '.join(detected_projects)}).")

    if not has_docker:
        dynamic_suggestions.append("- Add containerization experience (Docker / Kubernetes) to demonstrate cloud-native deployment.")
    if not has_aws:
        dynamic_suggestions.append("- Highlight cloud platform experience (AWS / Azure / GCP) to strengthen DevOps profile.")
    if not has_github:
        dynamic_suggestions.append("- Link active GitHub portfolio repositories showcasing clean code structure.")

    if not dynamic_suggestions:
        dynamic_suggestions.append(f"- Quantify impact in experience section with measurable outcomes tailored to {role}.")

    # GEMINI API CALL (Personalized AI Generation)
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("API key missing")

        prompt = f"""
Act as an executive hiring manager reviewing a resume for a {role} position.
Candidate Extracted Skills: {', '.join(skills[:10])}
Current ATS Quality Score: {score}/100

Provide a personalized, concise evaluation:
1. Top 2 specific strength observations based on extracted skills.
2. Top 2 actionable resume improvement recommendations for a {role} role.
3. 2 key skills to prioritize learning next.

Keep total length under 120 words. Format with clean bullet points. Do not use markdown headers or asterisks.
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
            text = text.replace("###", "").replace("**", "").replace("* ", "- ")
            final_text = f"[AI Tier - Gemini Powered]\n\n{text}"
            feedback_cache[cache_key] = final_text
            return final_text

        raise Exception("Empty Gemini response")

    except Exception as e:
        logger.info(f"Gemini API unavailable or missing ({str(e)}). Serving grounded local feedback tier.")

        nl = "\n"
        skills_summary = ", ".join([s.title() for s in skills[:6]]) if skills else "technical skills"
        local_feedback = (
            f"[Deterministic Rule-Based Tier]\n\n"
            f"Grounded Evaluation for {role} Profile:\n"
            f"- Extracted Core Competencies: {skills_summary}.\n"
            f"{nl.join(dynamic_suggestions[:3])}\n\n"
            f"Prioritized Next Actions:\n"
            f"- Add quantifiable metrics (e.g., % improvement, throughput) for recent software projects.\n"
            f"- Align resume keywords directly with target {role} position descriptions."
        )
        feedback_cache[cache_key] = local_feedback
        return local_feedback