import os
import uuid

from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect

from services.resume_service import analyze_resume
from services.report_service import generate_pdf_report
from models.database import save_resume

from services.ats_engine import calculate_ats_score

resume_bp = Blueprint(
    "resume",
    __name__
)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(
               ".", 1
           )[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # LOGIN REQUIRED
    if "user_id" not in session:
        return redirect("/login")

    # CHECK FILE
    if "resume" not in request.files:

        return render_template(
            "index.html",
            error="No file uploaded."
        )

    file = request.files["resume"]

    # GET JOB DESCRIPTION
    job_description = request.form.get(
        "job_description", ""
    )

    print(
        "\nJOB DESCRIPTION RECEIVED:\n",
        job_description
    )

    # EMPTY FILE CHECK
    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select a resume file."
        )

    # ONLY PDF ALLOWED
    if not allowed_file(
        file.filename
    ):
        return render_template(
            "index.html",
            error="Only PDF resumes are allowed. Please upload a PDF file."
        )

    # UNIQUE FILE NAME
    unique_filename = str(
        uuid.uuid4()
    ) + ".pdf"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    # CREATE FOLDER IF MISSING
    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    # SAVE FILE
    file.save(filepath)

    # ANALYZE RESUME
    result = analyze_resume(filepath)

    # ATS + JOB DESCRIPTION MATCHING
    ats_result = None

    if job_description.strip():

        ats_result = calculate_ats_score(
            result["raw_text"],
            job_description
        )

        print(
            "\nATS SCORE:",
            ats_result["ats_score"]
        )

    # SAVE FOR CURRENT USER
    save_resume(

        session["user_id"],
        file.filename,
        result["score"],
        result["role"],
        result["skills"]
    )

    # GENERATE PDF REPORT
    report_path = generate_pdf_report(

        file.filename,
        result["score"],
        result["role"],
        result["skills"],
        result["suggestions"],
        result["ai_feedback"],
        ats_result=ats_result
    )

    # SHOW RESULT PAGE
    return render_template(

        "result.html",

        skills=result["skills"],

        categorized_skills=result[
            "categorized_skills"
        ],

        score=result["score"],

        suggestions=result[
            "suggestions"
        ],

        predicted_role=result[
            "role"
        ],

        top_predictions=result[
            "top_predictions"
        ],

        report_path=report_path,

        ai_feedback=result[
            "ai_feedback"
        ],

        ats_result=ats_result
    )