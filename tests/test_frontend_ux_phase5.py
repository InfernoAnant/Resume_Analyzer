import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from utils.extensions import limiter

class FrontendUxPhase5TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        limiter.enabled = False
        self.client = app.test_client()

    def test_index_page_accessibility_and_tabs(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['username'] = 'testuser'

            # Test default hidden state (SHOW_RECRUITER_BATCH = False)
            app.config['SHOW_RECRUITER_BATCH'] = False
            res = c.get("/")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Analyze Your Resume", res.data)
            self.assertNotIn(b"Recruiter Batch", res.data)

            # Test enabled state (SHOW_RECRUITER_BATCH = True)
            app.config['SHOW_RECRUITER_BATCH'] = True
            res_enabled = c.get("/")
            self.assertEqual(res_enabled.status_code, 200)
            self.assertIn(b"Single Candidate", res_enabled.data)
            self.assertIn(b"Recruiter Batch", res_enabled.data)

    def test_result_page_executive_banner(self):
        with app.test_request_context():
            from flask import render_template
            top_preds = [
                {"role": "Backend Developer", "confidence": 98.5, "influential_keywords": ["python", "flask"]},
                {"role": "Full Stack Developer", "confidence": 85.0},
                {"role": "DevOps Engineer", "confidence": 70.0}
            ]
            html = render_template(
                "result.html",
                resume_quality_score=85,
                top_predictions=top_preds,
                suggestions=["Add Docker container experience"],
                report_path="storage/reports/sample.pdf",
                skills=["Python", "Flask", "SQL"],
                categorized_skills={"Backend": ["Python", "Flask"]},
                ai_feedback="Great resume",
                ats_result={"ats_score": 85, "explanation": "Score Breakdown: Matched 4/5 skills"}
            )
            self.assertIn("Resume Executive Summary", html)
            self.assertIn("Overall ATS Score", html)
            self.assertIn("Driven by:", html)

if __name__ == '__main__':
    unittest.main()
