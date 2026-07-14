import re

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.database import create_user
from models.database import get_user_by_email
from models.database import delete_user_account
from models.database import update_password

auth_bp = Blueprint(
    "auth",
    __name__
)

# REGISTER
@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
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
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip()
        new_password = request.form["new_password"].strip()
        confirm_password = request.form["confirm_password"].strip()

        # CHECK EMAIL EXISTS
        user = get_user_by_email(email)

        if not user:

            return render_template(
                "forgot_password.html",
                error="No account found with this email"
            )

        # PASSWORD MATCH CHECK
        if new_password != confirm_password:

            return render_template(
                "forgot_password.html",
                error="Passwords do not match"
            )

        # PASSWORD LENGTH
        if len(new_password) < 8:

            return render_template(
                "forgot_password.html",
                error="Password must be at least 8 characters"
            )

        # PASSWORD RULES
        if not re.search(r"[A-Z]", new_password):

            return render_template(
                "forgot_password.html",
                error="Password must contain one uppercase letter"
            )

        if not re.search(r"[a-z]", new_password):

            return render_template(
                "forgot_password.html",
                error="Password must contain one lowercase letter"
            )

        if not re.search(r"[0-9]", new_password):

            return render_template(
                "forgot_password.html",
                error="Password must contain one number"
            )

        # HASH PASSWORD
        hashed_password = generate_password_hash(new_password)

        # UPDATE PASSWORD
        update_password(email, hashed_password)

        return redirect("/login")

    return render_template("forgot_password.html")

# LOGOUT
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# DELETE ACCOUNT
@auth_bp.route("/delete-account")
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


# TEST ROUTE
@auth_bp.route("/test")
def test():

    return "AUTH ROUTE WORKING"