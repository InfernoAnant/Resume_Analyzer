from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

main_bp = Blueprint(
    "main",
    __name__
)

@main_bp.route("/")
def index():

    # if not logged in → go login page
    if "user_id" not in session:

        return redirect("/login")

    # if logged in → show homepage
    return render_template("index.html")