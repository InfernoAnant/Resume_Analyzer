import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from utils.extensions import db
from models.models import User, Resume, RoadmapProgress, PasswordResetToken
from models.repository import UserRepository, ResumeRepository, RoadmapRepository, TokenRepository
from services.resume_service import load_skills

class DataLayerPhase2TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_repository_user_flow(self):
        email = "phase2user@example.com"
        # Cleanup
        existing = UserRepository.get_by_email(email)
        if existing:
            UserRepository.delete_account(existing.id)

        user = UserRepository.create_user("phase2", email, "HashedPass123")
        self.assertIsNotNone(user.id)

        fetched = UserRepository.get_by_email(email)
        self.assertEqual(fetched.username, "phase2")

        # Test Save Resume
        resume = ResumeRepository.save_resume(user.id, "my_resume.pdf", 85, "Backend Engineer", ["Python", "Flask"])
        self.assertIsNotNone(resume.id)

        history = ResumeRepository.get_history(user.id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "my_resume.pdf")

        # Test Roadmap
        roadmap_sample = {
            "phases": [
                {"phase": 1, "skills": [{"name": "docker"}, {"name": "kubernetes"}]}
            ]
        }
        RoadmapRepository.save_roadmap(user.id, resume.id, roadmap_sample)
        latest_map = RoadmapRepository.get_latest_roadmap(user.id)
        self.assertIn(1, latest_map)

        # Cleanup
        UserRepository.delete_account(user.id)

    def test_skills_csv_lru_cache(self):
        skills1 = load_skills()
        skills2 = load_skills()
        self.assertIs(skills1, skills2, "load_skills() did not return cached object!")

if __name__ == '__main__':
    unittest.main()
