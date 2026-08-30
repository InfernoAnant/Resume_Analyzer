import re
import secrets
from datetime import datetime, timedelta

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from utils.extensions import limiter
from utils.email_service import send_reset_email

from models.database import create_user
from models.database import get_user_by_email
from models.database import delete_user_account
from models.database import update_password
from models.database import save_reset_token, get_valid_reset_token, mark_reset_token_used, get_user_by_id

auth_bp = Blueprint(
    "auth",
    __name__
)

# REGISTER
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
@limiter.limit("5 per minute")
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        # USERNAME VALIDATION
        if len(username) < 3:

            return render_template(
                "register.html",
                error="Username must be at least 3 characters"
            )

        if not re.match(
            r"^[A-Za-z0-9_]+$",
            username
        ):
            return render_template(
                "register.html",
                error="Username can contain only letters, numbers and underscore"
            )

        # EMAIL VALIDATION
        if not re.match(
            r"^[^@]+@[^@]+\.[^@]+$",
            email
        ):

            return render_template(
                "register.html",
                error="Please enter a valid email address"
            )

        # PASSWORD VALIDATION
        if len(password) < 8:

            return render_template(
                "register.html",
                error="Password must be at least 8 characters"
            )

        if not re.search(
            r"[A-Z]", password
        ):

            return render_template(
                "register.html",
                error="Password must contain one uppercase letter"
            )

        if not re.search(
            r"[a-z]", password
        ):

            return render_template(
                "register.html",
                error="Password must contain one lowercase letter"
            )

        if not re.search(
            r"[0-9]", password
        ):

            return render_template(
                "register.html",
                error="Password must contain one number"
            )

        # CHECK EXISTING EMAIL
        user = get_user_by_email(email)

        if user:

            return render_template(
                "register.html",
                error="Account already exists with this email"
            )

        # HASH PASSWORD
        hashed_password = generate_password_hash(password)

        # SAVE USER
        create_user(
            username,
            email,
            hashed_password
        )

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
@limiter.limit("5 per minute")
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        # EMAIL VALIDATION
        if not re.match(
            r"^[^@]+@[^@]+\.[^@]+$",
            email
        ):
            return render_template(
                "login.html",
                error="Please enter a valid email"
            )

        user = get_user_by_email(email)

        # USER NOT FOUND
        if not user:
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # PASSWORD CHECK
        if check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect("/")

        else:
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

    return render_template("login.html")

# FORGOT PASSWORD
@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
@limiter.limit("5 per minute")
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        # CHECK EMAIL EXISTS
        user = get_user_by_email(email)

        if user:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(minutes=30)
            save_reset_token(user[0], token, expires_at)

            reset_link = url_for("auth.reset_password", token=token, _external=True)
            try:
                send_reset_email(email, reset_link)
            except Exception:
                pass

        return render_template(
            "forgot_password.html",
            success="If an account exists with that email, we've sent a password reset link."
        )

    return render_template("forgot_password.html")

# RESET PASSWORD
@auth_bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
@limiter.limit("5 per minute")
def reset_password(token):

    record = get_valid_reset_token(token)
    if not record:
        return render_template(
            "forgot_password.html",
            error="Invalid or expired reset link. Please request a new one."
        )

    if request.method == "POST":

        new_password = request.form["new_password"].strip()
        confirm_password = request.form["confirm_password"].strip()

        # PASSWORD MATCH CHECK
        if new_password != confirm_password:

            return render_template(
                "reset_password.html",
                token=token,
                error="Passwords do not match"
            )

        # PASSWORD LENGTH
        if len(new_password) < 8:

            return render_template(
                "reset_password.html",
                token=token,
                error="Password must be at least 8 characters"
            )

        # PASSWORD RULES
        if not re.search(r"[A-Z]", new_password):

            return render_template(
                "reset_password.html",
                token=token,
                error="Password must contain one uppercase letter"
            )

        if not re.search(r"[a-z]", new_password):

            return render_template(
                "reset_password.html",
                token=token,
                error="Password must contain one lowercase letter"
            )

        if not re.search(r"[0-9]", new_password):

            return render_template(
                "reset_password.html",
                token=token,
                error="Password must contain one number"
            )

        # HASH PASSWORD
        hashed_password = generate_password_hash(new_password)

        # UPDATE PASSWORD
        user = get_user_by_id(record[1])
        update_password(user[2], hashed_password)

        # MARK USED
        mark_reset_token_used(record[0])

        return redirect("/login")

    return render_template("reset_password.html", token=token)

# LOGOUT
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# DELETE ACCOUNT
@auth_bp.route("/delete-account", methods=["POST"])
def delete_account():

    # CHECK LOGIN
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # DELETE USER + HISTORY
    delete_user_account(user_id)

    # CLEAR SESSION
    session.clear()

    # GO TO REGISTER PAGE
    return redirect("/register")

