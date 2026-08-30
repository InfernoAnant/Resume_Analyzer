from datetime import datetime
from utils.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, default=False, server_default='0', nullable=False)

    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    roadmap_items = db.relationship('RoadmapProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    reset_tokens = db.relationship('PasswordResetToken', backref='user', lazy=True, cascade='all, delete-orphan')

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String(50), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    roadmap_items = db.relationship('RoadmapProgress', backref='resume', lazy=True, cascade='all, delete-orphan')

class RoadmapProgress(db.Model):
    __tablename__ = 'roadmap_progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    skill = db.Column(db.String(100), nullable=False)
    phase = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.String(50), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.String(50), nullable=False)
    used = db.Column(db.Integer, default=0, nullable=False)
