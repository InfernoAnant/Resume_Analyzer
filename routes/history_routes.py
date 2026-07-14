from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import session
from flask import request

from models.database import (get_history, delete_resume)

history_bp = Blueprint(
    "history",
    __name__
)

# HISTORY PAGE
@history_bp.route("/history")
def history():

    # login required
    if "user_id" not in session:
        return redirect("/login")

    # get only current user history
    records = get_history(
        session["user_id"]
    )

    return render_template(
        "history.html",
        records=records
    )

# DELETE RECORD (SAFE POST)
@history_bp.route(
    "/delete/<int:resume_id>",
    methods=["POST"]
)
def delete_record(resume_id):

    # login required
    if "user_id" not in session:
        return redirect("/login")

    # delete only current user's record
    delete_resume(
        resume_id,
        session["user_id"]
    )

    return redirect(
        "/history"
    )