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

    # ROADMAP PROGRESS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_progress(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            resume_id INTEGER,
            skill TEXT,
            phase INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(resume_id) REFERENCES resumes(id)
        )
    """)

    # PASSWORD RESET TOKENS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            expires_at TEXT,
            used INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
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


# SAVE ROADMAP
def save_roadmap(user_id, resume_id, roadmap):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for phase_info in roadmap["phases"]:

        phase_num = phase_info["phase"]

        for skill_info in phase_info["skills"]:

            cursor.execute("""
                INSERT INTO roadmap_progress(
                    user_id,
                    resume_id,
                    skill,
                    phase,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                resume_id,
                skill_info["name"],
                phase_num,
                "pending",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ))

    conn.commit()
    conn.close()


# GET LATEST ROADMAP
def get_latest_roadmap(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(resume_id) FROM roadmap_progress
        WHERE user_id=?
    """, (user_id,))
    
    row = cursor.fetchone()
    
    if not row or not row[0]:
        conn.close()
        return None
        
    latest_resume_id = row[0]

    cursor.execute("""
        SELECT skill, phase, status 
        FROM roadmap_progress
        WHERE user_id=? AND resume_id=?
        ORDER BY phase ASC
    """, (user_id, latest_resume_id))

    records = cursor.fetchall()

    conn.close()

    roadmap_data = {}
    for skill, phase, status in records:
        if phase not in roadmap_data:
            roadmap_data[phase] = []
        roadmap_data[phase].append({
            "name": skill,
            "status": status
        })

    return roadmap_data


# UPDATE SKILL STATUS
def update_skill_status(user_id, skill, status):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(resume_id) FROM roadmap_progress
        WHERE user_id=?
    """, (user_id,))
    
    row = cursor.fetchone()
    
    if row and row[0]:
        latest_resume_id = row[0]

        cursor.execute("""
            UPDATE roadmap_progress
            SET status=?
            WHERE user_id=? AND resume_id=? AND skill=?
        """, (
            status,
            user_id,
            latest_resume_id,
            skill
        ))

    conn.commit()
    conn.close()


# AUTO COMPLETE SKILLS
def auto_complete_skills(user_id, resume_skills):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(resume_id) FROM roadmap_progress
        WHERE user_id=?
    """, (user_id,))
    
    row = cursor.fetchone()
    
    if row and row[0]:
        latest_resume_id = row[0]

        for skill in resume_skills:
            skill = skill.lower().strip()
            
            cursor.execute("""
                UPDATE roadmap_progress
                SET status='completed'
                WHERE user_id=? AND resume_id=? AND skill=?
            """, (
                user_id,
                latest_resume_id,
                skill
            ))

    conn.commit()
    conn.close()


# SAVE RESET TOKEN
def save_reset_token(user_id, token, expires_at):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO password_reset_tokens(
            user_id, token, expires_at, used
        )
        VALUES (?, ?, ?, 0)
    """, (
        user_id,
        token,
        expires_at.strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# GET VALID RESET TOKEN
def get_valid_reset_token(token):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM password_reset_tokens
        WHERE token=? AND used=0
    """, (token,))

    record = cursor.fetchone()
    conn.close()

    if record:
        expires_at = datetime.strptime(record[3], "%Y-%m-%d %H:%M:%S")
        if expires_at > datetime.now():
            return record

    return None


# MARK RESET TOKEN USED
def mark_reset_token_used(token_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE password_reset_tokens
        SET used=1
        WHERE id=?
    """, (token_id,))

    conn.commit()
    conn.close()


# FIND USER BY ID
def get_user_by_id(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    return user
