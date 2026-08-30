import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from utils.role_predictor import predict_role
from utils.skill_extractor import extract_skills
from services.resume_service import load_skills
from services.jd_matcher import compare_resume_with_jd, calculate_semantic_similarity
from services.ats_engine import calculate_ats_score
from utils.ai_feedback import get_ai_feedback

class NlpMlPhase3TestCase(unittest.TestCase):

    def test_calibrated_role_predictor_and_explainability(self):
        resume_text = "Experienced Senior Python Developer building scalable REST APIs using Flask, PostgreSQL, Docker, and Kubernetes on AWS."
        predictions = predict_role(resume_text)
        
        self.assertGreater(len(predictions), 0)
        top = predictions[0]
        self.assertIn("role", top)
        self.assertIn("confidence", top)
        self.assertGreaterEqual(top["confidence"], 1.0)
        self.assertLessEqual(top["confidence"], 100.0)
        self.assertIn("influential_keywords", top)
        self.assertIsInstance(top["influential_keywords"], list)

    def test_semantic_skill_extraction_and_synonyms(self):
        skills_db = load_skills()
        # Resume text containing aliases "k8s", "postgres", "rest apis"
        raw_text = "Built services with python, flask, postgres, k8s, and rest apis"
        found_skills, categorized = extract_skills(raw_text, skills_db)
        
        found_lower = [s.lower() for s in found_skills]
        self.assertIn("python", found_lower)
        self.assertIn("flask", found_lower)
        self.assertIn("postgresql", found_lower, "Synonym 'postgres' was not resolved to 'postgresql'!")
        self.assertIn("kubernetes", found_lower, "Synonym 'k8s' was not resolved to 'kubernetes'!")
        self.assertIn("rest api", found_lower, "Synonym 'rest apis' was not resolved to 'rest api'!")

    def test_semantic_jd_matching_and_explainability(self):
        resume_text = "Backend engineer specializing in Python, Flask, Microservices, PostgreSQL, and Docker."
        job_description = "We are seeking a Backend Developer skilled in Python, Flask, Database design (PostgreSQL), and Docker container deployment."
        
        sim_score = calculate_semantic_similarity(resume_text, job_description)
        self.assertGreater(sim_score, 0.2)

        ats_res = calculate_ats_score(resume_text, job_description=job_description)
        self.assertIn("ats_score", ats_res)
        self.assertIn("semantic_similarity", ats_res)
        self.assertIn("explanation", ats_res)
        self.assertIn("Score Breakdown", ats_res["explanation"])

    def test_grounded_ai_feedback(self):
        feedback = get_ai_feedback(["python", "flask"], 45.0, "Backend Developer")
        self.assertTrue(feedback.startswith("[AI Tier") or feedback.startswith("[Deterministic Rule-Based Tier]"))
        self.assertIn("Backend Developer", feedback)

if __name__ == '__main__':
    unittest.main()
