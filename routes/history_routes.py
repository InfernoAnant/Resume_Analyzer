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

from models.models import Resume

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

# COMPARE TWO RESUME VERSIONS
@history_bp.route("/compare/<int:id1>/<int:id2>")
def compare_versions(id1, id2):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    r1 = Resume.query.filter_by(id=id1, user_id=user_id).first()
    r2 = Resume.query.filter_by(id=id2, user_id=user_id).first()

    if not r1 or not r2:
        return redirect("/history")

    skills1 = set([s.strip().lower() for s in r1.skills.split(",") if s.strip()])
    skills2 = set([s.strip().lower() for s in r2.skills.split(",") if s.strip()])

    score_delta = r2.score - r1.score
    added_skills = list(skills2 - skills1)
    removed_skills = list(skills1 - skills2)
    retained_skills = list(skills1 & skills2)

    diff_data = {
        "r1": r1,
        "r2": r2,
        "score_delta": score_delta,
        "added_skills": added_skills,
        "removed_skills": removed_skills,
        "retained_skills": retained_skills
    }

    return render_template("compare.html", diff=diff_data)

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