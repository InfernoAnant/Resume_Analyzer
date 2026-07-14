from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from models.database import get_dashboard_data
from services.chart_service import generate_dashboard_chart

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
def dashboard():

    # LOGIN REQUIRED
    if "user_id" not in session:
        return redirect("/login")

    # GET CURRENT USER DATA
    data = get_dashboard_data(
        session["user_id"]
    )

    # IF NO DATA → GO HOME
    if not data:
        return redirect("/")

    # EXTRACT SCORES + ROLES
    scores = [
        row[0] for row in data
    ]

    roles = [
        row[1] for row in data
    ]

    # CALCULATE ANALYTICS
    total_resumes = len(scores)
    average_score = sum(scores) / len(scores)

    most_common_role = max(
        set(roles),
        key=roles.count
    )

    # GENERATE CHART
    chart_path = generate_dashboard_chart(roles)

    # RENDER DASHBOARD
    return render_template(

        "dashboard.html",

        total_resumes=total_resumes,

        average_score=round(average_score,2),

        most_common_role=most_common_role,
        chart_path=chart_path
    )