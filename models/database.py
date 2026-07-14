import sqlite3
import os
from datetime import datetime

DB_NAME = os.path.abspath("resume.db")

# INIT DATABASE
def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # RESUMES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            score INTEGER,
            role TEXT,
            skills TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# REGISTER USER
def create_user(username, email, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO users(
            username,
            email,
            password
        )
        VALUES (?, ?, ?)

    """, (
        username,
        email,
        password
    ))

    conn.commit()
    conn.close()


# FIND USER BY EMAIL
def get_user_by_email(email):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user


# SAVE RESUME
def save_resume(user_id, filename, score, role, skills):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO resumes(
            user_id,
            filename,
            score,
            role,
            skills,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        user_id,
        filename,
        score,
        role,
        ", ".join(skills),

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()
    conn.close()


# HISTORY
def get_history(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id, filename, score, role, created_at
        FROM resumes
        WHERE user_id=?
        ORDER BY id DESC

    """, (user_id,))

    records = cursor.fetchall()

    conn.close()

    return records


# DASHBOARD
def get_dashboard_data(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT score, role
        FROM resumes
        WHERE user_id=?

    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


# DELETE SINGLE RESUME
def delete_resume(resume_id, user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM resumes
        WHERE id=? AND user_id=?

    """, (
        resume_id,
        user_id
    ))

    conn.commit()
    conn.close()


# DELETE USER ACCOUNT
def delete_user_account(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Delete resume history first
    cursor.execute("""

        DELETE FROM resumes
        WHERE user_id=?

    """, (user_id,))

    # Delete user account
    cursor.execute("""

        DELETE FROM users
        WHERE id=?

    """, (user_id,))

    conn.commit()
    conn.close()

# UPDATE PASSWORD
def update_password(email, new_password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users
        SET password=?
        WHERE email=?

    """, (
        new_password,
        email
    ))

    conn.commit()
    conn.close()
