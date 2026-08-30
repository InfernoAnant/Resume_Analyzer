import os
import uuid

from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect

from services.resume_service import analyze_resume
from services.report_service import generate_pdf_report
from models.database import save_resume, auto_complete_skills
from utils.pdf_reader import PDFExtractionError

from services.ats_engine import calculate_ats_score
from services.roadmap_generator import generate_roadmap, render_roadmap_svg
from models.database import save_roadmap, get_history

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

    # GET JOB DESCRIPTION & TARGET ROLE
    job_description = request.form.get("job_description", "").strip()
    target_role = request.form.get("target_role", "").strip()

    # AUTO-DETECT ROLE IN JD FIELD
    if not target_role and job_description:
        from utils.role_skills_mapping import ROLE_SKILLS
        if job_description.lower() in ROLE_SKILLS:
            target_role = job_description.lower()
            job_description = ""

    print(
        "\nJOB DESCRIPTION RECEIVED:\n",
        job_description,
        "\nTARGET ROLE RECEIVED:\n",
        target_role
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

    with open(filepath, "rb") as f:
        header = f.read(5)
    
    if header != b"%PDF-":
        os.remove(filepath)
        return render_template(
            "index.html",
            error="Invalid file format. The file is not a valid PDF."
        )

    # ANALYZE RESUME
    try:
        result = analyze_resume(filepath)
    except PDFExtractionError as e:
        os.remove(filepath)
        return render_template(
            "index.html",
            error=str(e)
        )

    # ATS + JOB DESCRIPTION MATCHING
    ats_result = None

    if job_description.strip() or target_role:

        ats_result = calculate_ats_score(
            result["raw_text"],
            job_description=job_description,
            target_role=target_role
        )

        print(
            "\nATS SCORE:",
            ats_result["ats_score"]
        )

    # SAVE FOR CURRENT USER
    save_resume(
        session["user_id"],
        file.filename,
        result["resume_quality_score"],
        result["role"],
        result["skills"]
    )

    roadmap_data = None
    if ats_result and ats_result.get("missing_skills"):
        # Generate roadmap
        roadmap_data = generate_roadmap(
            ats_result["missing_skills"],
            ats_result.get("matched_skills", []) + result["skills"],
            result["role"]
        )
        
        # Render the SVG
        # SVG rendering removed in favor of native HTML\n        pass
        
        # Save to DB
        records = get_history(session["user_id"])
        if records:
            resume_id = records[0][0]
            save_roadmap(session["user_id"], resume_id, roadmap_data)

    # AUTO COMPLETE SKILLS FOR ROADMAP
    auto_complete_skills(
        session["user_id"],
        result["skills"]
    )

    # GENERATE PDF REPORT
    report_path = generate_pdf_report(

        file.filename,
        result["resume_quality_score"],
        result["role"],
        result["skills"],
        result["suggestions"],
        result["ai_feedback"],
        ats_result=ats_result,
        roadmap_data=roadmap_data
    )

    # SHOW RESULT PAGE
    return render_template(

        "result.html",

        skills=result["skills"],

        categorized_skills=result[
            "categorized_skills"
        ],

        resume_quality_score=result["resume_quality_score"],

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

        ats_result=ats_result,
        roadmap_data=roadmap_data
    )