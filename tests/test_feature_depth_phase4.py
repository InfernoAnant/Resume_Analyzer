import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import io
import sqlite3
from app import app
from werkzeug.security import generate_password_hash
from models.database import DB_NAME, save_resume
from services.roadmap_generator import generate_roadmap
from utils.extensions import limiter

class FeatureDepthPhase4TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        limiter.enabled = False
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db_name = DB_NAME

        # Setup test user
        self.test_email = "phase4user@example.com"
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE email=?", (self.test_email,))
        c.execute("INSERT INTO users (username, email, password, email_verified) VALUES (?, ?, ?, 0)",
                  ("phase4user", self.test_email, generate_password_hash("Password123")))
        conn.commit()
        c.execute("SELECT id FROM users WHERE email=?", (self.test_email,))
        self.test_user_id = c.fetchone()[0]
        conn.close()

    def tearDown(self):
        self.app_context.pop()

    def test_resume_version_comparison_route(self):
        # Save version 1 and version 2
        r1 = save_resume(self.test_user_id, "v1.pdf", 60, "Backend Developer", ["python", "flask"])
        r2 = save_resume(self.test_user_id, "v2.pdf", 80, "Backend Developer", ["python", "flask", "docker", "postgresql"])

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
                sess['username'] = 'phase4user'

            res = c.get(f"/compare/{r1.id}/{r2.id}")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Score Delta:", res.data)
            self.assertIn(b"+20%", res.data)
            self.assertIn(b"docker", res.data)

    def test_recruiter_batch_analysis_ranking(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
                sess['username'] = 'phase4user'

            # Upload 2 pdf resumes
            pdf1 = (io.BytesIO(b"%PDF-1.4\nPython Flask REST API Docker PostgreSQL"), "backend.pdf")
            pdf2 = (io.BytesIO(b"%PDF-1.4\nHTML CSS Javascript"), "frontend.pdf")

            res = c.post("/batch-analyze", data={
                "job_description": "Looking for Backend Engineer with Python, Flask, REST API, Docker, PostgreSQL",
                "resumes": [pdf1, pdf2]
            }, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Recruiter Batch Leaderboard", res.data)
            self.assertIn(b"#1", res.data)

    def test_rich_roadmap_resource_links(self):
        roadmap = generate_roadmap(["python", "docker", "postgresql"], ["html"], "Backend Developer")
        self.assertIn("phases", roadmap)
        self.assertGreater(len(roadmap["phases"]), 0)
        skill_sample = roadmap["phases"][0]["skills"][0]
        self.assertIn("resource_url", skill_sample)
        self.assertIn("resource_title", skill_sample)
        self.assertTrue(skill_sample["resource_url"].startswith("http"))

if __name__ == '__main__':
    unittest.main()
