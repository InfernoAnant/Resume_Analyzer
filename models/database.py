import os
from utils.extensions import db
from models.repository import UserRepository, ResumeRepository, RoadmapRepository, TokenRepository

DB_NAME = os.path.abspath("resume.db")

def init_db():
    db.create_all()

def create_user(username, email, password):
    user = UserRepository.create_user(username, email, password)
    return (user.id, user.username, user.email, user.password)

def get_user_by_email(email):
    user = UserRepository.get_by_email(email)
    if user:
        return (user.id, user.username, user.email, user.password)
    return None

def get_user_by_id(user_id):
    user = UserRepository.get_by_id(user_id)
    if user:
        return (user.id, user.username, user.email, user.password)
    return None

def save_resume(user_id, filename, score, role, skills):
    return ResumeRepository.save_resume(user_id, filename, score, role, skills)

def get_history(user_id):
    return ResumeRepository.get_history(user_id)

def get_dashboard_data(user_id):
    return ResumeRepository.get_dashboard_data(user_id)

def delete_resume(resume_id, user_id):
    return ResumeRepository.delete_resume(resume_id, user_id)

def delete_user_account(user_id):
    return UserRepository.delete_account(user_id)

def update_password(email, new_password):
    return UserRepository.update_password(email, new_password)

def save_roadmap(user_id, resume_id, roadmap):
    return RoadmapRepository.save_roadmap(user_id, resume_id, roadmap)

def get_latest_roadmap(user_id):
    return RoadmapRepository.get_latest_roadmap(user_id)

def update_skill_status(user_id, skill, status):
    return RoadmapRepository.update_skill_status(user_id, skill, status)

def auto_complete_skills(user_id, resume_skills):
    return RoadmapRepository.auto_complete_skills(user_id, resume_skills)

def save_reset_token(user_id, token, expires_at):
    return TokenRepository.save_reset_token(user_id, token, expires_at)

def get_valid_reset_token(token):
    return TokenRepository.get_valid_reset_token(token)

def mark_reset_token_used(token_id):
    return TokenRepository.mark_reset_token_used(token_id)
