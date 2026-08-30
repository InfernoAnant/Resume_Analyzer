import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from utils.extensions import limiter
from services.resume_service import load_skills
from utils.skill_extractor import extract_skills
from services.ats_engine import calculate_ats_score

class AppBaselineTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        limiter.enabled = False
        self.client = app.test_client()

    def test_health_and_login_routes(self):
        res = self.client.get("/login")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_skill_extraction_pipeline(self):
        skills_db = load_skills()
        self.assertGreater(len(skills_db), 0)
        
        resume_text = "Experienced in Python, Flask, REST API, Docker, PostgreSQL, and Kubernetes"
        skills, categorized = extract_skills(resume_text, skills_db)
        
        skills_lower = [s.lower() for s in skills]
        self.assertIn("python", skills_lower)
        self.assertIn("flask", skills_lower)
        self.assertIn("docker", skills_lower)

    def test_ats_score_calculation(self):
        resume = "Python, Flask, REST API, PostgreSQL"
        jd = "Python, Flask, REST API, PostgreSQL, Docker, Kubernetes"
        
        result = calculate_ats_score(resume, job_description=jd)
        self.assertIn("ats_score", result)
        self.assertGreater(result["ats_score"], 0)
        self.assertIn("matched_skills", result)
        self.assertIn("missing_skills", result)

if __name__ == '__main__':
    unittest.main()
