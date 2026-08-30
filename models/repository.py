import secrets
from datetime import datetime
from utils.extensions import db
from models.models import User, Resume, RoadmapProgress, PasswordResetToken

class UserRepository:
    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def update_password(email, new_password):
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_account(user_id):
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

class ResumeRepository:
    @staticmethod
    def save_resume(user_id, filename, score, role, skills):
        skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
        resume = Resume(
            user_id=user_id,
            filename=filename,
            score=score,
            role=role,
            skills=skills_str
        )
        db.session.add(resume)
        db.session.commit()
        return resume

    @staticmethod
    def get_history(user_id):
        resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.id.desc()).all()
        return [(r.id, r.filename, r.score, r.role, r.created_at) for r in resumes]

    @staticmethod
    def get_dashboard_data(user_id):
        resumes = Resume.query.filter_by(user_id=user_id).all()
        return [(r.score, r.role) for r in resumes]

    @staticmethod
    def delete_resume(resume_id, user_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if resume:
            db.session.delete(resume)
            db.session.commit()
            return True
        return False

class RoadmapRepository:
    @staticmethod
    def save_roadmap(user_id, resume_id, roadmap):
        for phase_info in roadmap.get("phases", []):
            phase_num = phase_info["phase"]
            for skill_info in phase_info.get("skills", []):
                item = RoadmapProgress(
                    user_id=user_id,
                    resume_id=resume_id,
                    skill=skill_info["name"],
                    phase=phase_num,
                    status="pending"
                )
                db.session.add(item)
        db.session.commit()

    @staticmethod
    def get_latest_roadmap(user_id):
        latest_resume = db.session.query(db.func.max(RoadmapProgress.resume_id))\
            .filter(RoadmapProgress.user_id == user_id).scalar()
        if not latest_resume:
            return None

        records = RoadmapProgress.query.filter_by(user_id=user_id, resume_id=latest_resume)\
            .order_by(RoadmapProgress.phase.asc()).all()

        roadmap_data = {}
        for r in records:
            if r.phase not in roadmap_data:
                roadmap_data[r.phase] = []
            roadmap_data[r.phase].append({
                "name": r.skill,
                "status": r.status
            })
        return roadmap_data

    @staticmethod
    def update_skill_status(user_id, skill, status):
        latest_resume = db.session.query(db.func.max(RoadmapProgress.resume_id))\
            .filter(RoadmapProgress.user_id == user_id).scalar()
        if latest_resume:
            RoadmapProgress.query.filter_by(user_id=user_id, resume_id=latest_resume, skill=skill)\
                .update({"status": status})
            db.session.commit()

    @staticmethod
    def auto_complete_skills(user_id, resume_skills):
        latest_resume = db.session.query(db.func.max(RoadmapProgress.resume_id))\
            .filter(RoadmapProgress.user_id == user_id).scalar()
        if latest_resume:
            for skill in resume_skills:
                skill_clean = skill.lower().strip()
                RoadmapProgress.query.filter_by(user_id=user_id, resume_id=latest_resume, skill=skill_clean)\
                    .update({"status": "completed"})
            db.session.commit()

class TokenRepository:
    @staticmethod
    def save_reset_token(user_id, token, expires_at):
        # Single flight: invalidate prior unused tokens
        PasswordResetToken.query.filter_by(user_id=user_id, used=0).update({"used": 1})
        
        expires_str = expires_at.strftime("%Y-%m-%d %H:%M:%S") if isinstance(expires_at, datetime) else str(expires_at)
        prt = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_str, used=0)
        db.session.add(prt)
        db.session.commit()
        return prt

    @staticmethod
    def get_valid_reset_token(token):
        tokens = PasswordResetToken.query.filter_by(used=0).all()
        for record in tokens:
            if secrets.compare_digest(record.token, token):
                expires_at = datetime.strptime(record.expires_at, "%Y-%m-%d %H:%M:%S")
                if expires_at > datetime.now():
                    return (record.id, record.user_id, record.token, record.expires_at, record.used)
        return None

    @staticmethod
    def mark_reset_token_used(token_id):
        PasswordResetToken.query.filter_by(id=token_id).update({"used": 1})
        db.session.commit()
