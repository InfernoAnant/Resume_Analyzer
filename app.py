from flask import Flask
import os
from dotenv import load_dotenv

from flask_wtf.csrf import CSRFProtect
from utils.extensions import limiter

from routes.main_routes import main_bp
from routes.resume_routes import resume_bp
from routes.history_routes import history_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from models.database import init_db

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

secret = os.getenv("SECRET_KEY")
if not secret:
    raise RuntimeError("SECRET_KEY environment variable is not set")
app.secret_key = secret

csrf = CSRFProtect(app)
limiter.init_app(app)

init_db()

app.register_blueprint(main_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(history_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
if __name__ == "__main__":
    app.run()