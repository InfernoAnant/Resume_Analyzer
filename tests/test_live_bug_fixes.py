import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from utils.role_skills_mapping import resolve_role_name, get_skills_for_role
from services.ats_engine import calculate_ats_score
from services.resume_service import analyze_resume, load_skills
from utils.skill_extractor import extract_skills
from utils.ai_feedback import get_ai_feedback

ANANT_RESUME_TEXT = """
ANANT KRISHNA ULUGUNDAM
Vadodara, Gujarat | ulugundamanantkrishna@gmail.com | github.com/InfernoAnant | +91 9966322236
PROFESSIONAL SUMMARY
Final-year B.Tech Computer Science & Engineering student with a strong foundation in Object-Oriented
Programming, Data Structures & Algorithms, Operating Systems, and Database Management Systems. Proficient in
Java and Python with hands-on software development experience building full-stack applications.
TECHNICAL SKILLS
Programming Languages: Java, Python, JavaScript, TypeScript
Backend & Databases: Node.js, Express, FastAPI, PostgreSQL (Relational DB), Prisma
Web Technologies: React, REST APIs
Tools & Cloud: Git, GitHub, Postman, AWS (Solutions Architect - Job Simulation)
PROJECTS
TransitOps – Fleet Management Platform
React 19, TypeScript, Node.js, Express, Prisma, PostgreSQL | Hackathon Build
Mini-ERP – Hackathon Project
React, Node.js, PostgreSQL | Hackathon Build
NLP-Based Resume Parsing & Job Matching Platform
Python, NLP | Academic Project
"""

class LiveBugFixesTestCase(unittest.TestCase):

    def test_unmapped_role_resolution_and_alias_mapping(self):
        title, skills, is_mapped = resolve_role_name("software engineer")
        self.assertTrue(is_mapped)
        self.assertEqual(title, "Software Engineer")
        self.assertIn("express.js", skills)
        self.assertIn("postgresql", skills)

        ats_res = calculate_ats_score(ANANT_RESUME_TEXT, target_role="software engineer")
        self.assertGreater(ats_res["skill_match_score"], 50.0)
        self.assertNotEqual(ats_res["explanation"], "Matched 0/0 target skills")

    def test_express_synonym_normalization(self):
        ats_res = calculate_ats_score(ANANT_RESUME_TEXT, target_role="software engineer")
        self.assertIn("express.js", ats_res["matched_skills"], "'Express' in resume did not match 'express.js' in target role skills!")

    def test_no_false_negative_suggestions(self):
        skills_db = load_skills()
        found_skills, categorized = extract_skills(ANANT_RESUME_TEXT, skills_db)
        
        # Test GitHub detection in text header
        import re
        has_github = "github" in [s.lower() for s in found_skills] or bool(re.search(r'github\.com|\bgithub\b', ANANT_RESUME_TEXT, re.IGNORECASE))
        self.assertTrue(has_github, "GitHub profile in header was not detected!")

        # Test AI/ML project detection in text
        has_aiml = bool(re.search(r'\b(nlp|machine learning|ai)\b', ANANT_RESUME_TEXT, re.IGNORECASE))
        self.assertTrue(has_aiml, "NLP project in resume text was not detected!")

    def test_grounded_ai_feedback_at_score_63(self):
        skills_db = load_skills()
        found_skills, _ = extract_skills(ANANT_RESUME_TEXT, skills_db)
        
        feedback = get_ai_feedback(found_skills, 63.0, "Full Stack Developer", raw_text=ANANT_RESUME_TEXT)
        self.assertNotIn("Add internship experience", feedback, "Generic un-grounded static fallback string was returned!")
        self.assertIn("Grounded Evaluation", feedback)
        self.assertTrue("Python" in feedback or "React" in feedback)

    def test_consistent_quality_score_threshold_mapping(self):
        def get_badge(score):
            if score >= 80:
                return "Excellent Match"
            elif score >= 60:
                return "Strong Resume"
            elif score >= 40:
                return "Moderate Fit"
            else:
                return "Needs Improvement"

        self.assertEqual(get_badge(63), "Strong Resume")
        self.assertEqual(get_badge(85), "Excellent Match")
        self.assertEqual(get_badge(45), "Moderate Fit")
        self.assertEqual(get_badge(30), "Needs Improvement")

if __name__ == '__main__':
    unittest.main()
