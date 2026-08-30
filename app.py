from flask import Flask
import os
from dotenv import load_dotenv

from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from utils.extensions import limiter, db, migrate
from utils.logger import logger

from routes.main_routes import main_bp
from routes.resume_routes import resume_bp
from routes.history_routes import history_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
import models.models  # Register models with SQLAlchemy

import config

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["SHOW_RECRUITER_BATCH"] = getattr(config, "SHOW_RECRUITER_BATCH", False)

@app.context_processor
def inject_feature_flags():
    return dict(show_recruiter_batch=app.config.get("SHOW_RECRUITER_BATCH", False))

# DATABASE CONFIG (Swappable for Postgres/MySQL)
db_url = os.getenv("DATABASE_URL", "sqlite:///" + os.path.abspath("resume.db"))
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

# SESSION & COOKIE SECURITY
is_prod = os.getenv("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = is_prod

secret = os.getenv("SECRET_KEY")
if not secret:
    logger.error("SECRET_KEY environment variable is not set!")
    raise RuntimeError("SECRET_KEY environment variable is not set")
app.secret_key = secret

# TALISMAN SECURITY HEADERS
csp = {
    'default-src': '\'self\'',
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://cdn.jsdelivr.net'
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://cdn.jsdelivr.net'
    ],
    'font-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net'
    ],
    'img-src': [
        '\'self\'',
        'data:'
    ]
}

talisman = Talisman(
    app,
    content_security_policy=csp,
    force_https=is_prod,
    session_cookie_secure=is_prod
)

csrf = CSRFProtect(app)
limiter.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(history_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run()