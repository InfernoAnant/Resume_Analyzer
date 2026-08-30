import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import io
import secrets
from app import app
from models.database import create_user, get_user_by_email, save_reset_token, get_valid_reset_token, DB_NAME
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta

from utils.extensions import limiter

class SecurityPhase1TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        limiter.enabled = False
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db_name = DB_NAME

        # Create test user
        self.test_email = "secuser@example.com"
        self.test_password = "Password123"
        self.hashed_pw = generate_password_hash(self.test_password)
        
        # Clean existing test user if present
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE email=?", (self.test_email,))
        c.execute("INSERT INTO users (username, email, password, email_verified) VALUES (?, ?, ?, 0)",
                  ("secuser", self.test_email, self.hashed_pw))
        conn.commit()
        
        c.execute("SELECT id FROM users WHERE email=?", (self.test_email,))
        self.test_user_id = c.fetchone()[0]
        conn.close()

    def tearDown(self):
        self.app_context.pop()

    def test_session_fixation_mitigation(self):
        c = self.client
        with c.session_transaction() as sess:
            sess['pre_login'] = 'should_be_cleared'

        c.post('/login', data={
            'email': self.test_email,
            'password': self.test_password
        }, follow_redirects=True)

        with c.session_transaction() as sess:
            self.assertNotIn('pre_login', sess)
            self.assertEqual(sess.get('user_id'), self.test_user_id)

    def test_account_deletion_requires_password(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
                sess['username'] = 'secuser'

            # Attempt deletion with wrong password
            res_wrong = c.post('/delete-account', data={'password': 'WrongPassword123'}, follow_redirects=True)
            user_still_exists = get_user_by_email(self.test_email)
            self.assertIsNotNone(user_still_exists)

            # Attempt deletion with correct password
            res_correct = c.post('/delete-account', data={'password': self.test_password}, follow_redirects=True)
            user_deleted = get_user_by_email(self.test_email)
            self.assertIsNone(user_deleted)

    def test_single_flight_password_reset_token(self):
        expires_at = datetime.now() + timedelta(minutes=30)
        token1 = secrets.token_urlsafe(32)
        token2 = secrets.token_urlsafe(32)

        save_reset_token(self.test_user_id, token1, expires_at)
        rec1 = get_valid_reset_token(token1)
        self.assertIsNotNone(rec1)

        # Issue second token -> first token must be invalidated
        save_reset_token(self.test_user_id, token2, expires_at)
        rec1_after = get_valid_reset_token(token1)
        rec2_after = get_valid_reset_token(token2)

        self.assertIsNone(rec1_after, "Prior reset token was not invalidated when new token was issued!")
        self.assertIsNotNone(rec2_after, "New reset token is not valid!")

    def test_account_lockout_after_failed_logins(self):
        lockout_email = "lockout@example.com"
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE email=?", (lockout_email,))
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  ("lockoutuser", lockout_email, generate_password_hash("Password123")))
        conn.commit()
        conn.close()

        # Fail 5 consecutive login attempts
        for _ in range(5):
            self.client.post('/login', data={'email': lockout_email, 'password': 'WrongPassword1'})

        # 6th attempt with correct password should still be locked out
        res = self.client.post('/login', data={'email': lockout_email, 'password': 'Password123'})
        self.assertIn(b"Account temporarily locked", res.data)

    def test_pdf_upload_security_and_non_servable_path(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
                sess['username'] = 'secuser'

            # Test non-PDF header file upload
            fake_file = (io.BytesIO(b"NOT_A_PDF_FILE_HEADER"), "test.pdf")
            res = c.post('/analyze', data={'resume': fake_file}, follow_redirects=True)
            self.assertIn(b"Invalid file format", res.data)

    def test_security_headers_present(self):
        res = self.client.get('/')
        self.assertIn('X-Content-Type-Options', res.headers)
        self.assertIn('X-Frame-Options', res.headers)

if __name__ == '__main__':
    unittest.main()
