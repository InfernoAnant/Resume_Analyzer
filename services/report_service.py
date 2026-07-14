import os

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors


def generate_pdf_report(
    filename,
    ats_score,
    predicted_role,
    found_skills,
    suggestions,
    ai_feedback=None,
    chart_path=None,
    ats_result=None
):

    base_name = os.path.splitext(filename)[0]

    os.makedirs("static/reports", exist_ok=True)

    report_path = os.path.join(
        "static",
        "reports",
        f"{base_name}_report.pdf"
    )

    doc = SimpleDocTemplate(
        report_path, pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    data = [
        ["Filename", filename],
        ["ATS Score", f"{ats_score}%"],
        ["Recommended Role", predicted_role]
    ]

    table = Table(
        data, colWidths=[180, 300]
    )

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ])
    )

    elements.append(table)

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            ", ".join(found_skills),
            styles["BodyText"]
        )
    )

    # NEW ATS/JOB DESCRIPTION MATCH SECTION
    if ats_result:

        elements.append(Spacer(1,20))

        elements.append(
            Paragraph(
                "<b>Job Description Match Analysis</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"Match Score: {ats_result['ats_score']}%",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1,10))

        elements.append(
            Paragraph(
                "<b>Matched Skills</b>",
                styles["BodyText"]
            )
        )

        for skill in ats_result["matched_skills"]:
            elements.append(
                Paragraph(
                    f"• {skill}",
                    styles["BodyText"]
                )
            )

        elements.append(Spacer(1,10))

        elements.append(
            Paragraph(
                "<b>Missing Skills</b>",
                styles["BodyText"]
            )
        )

        for skill in ats_result["missing_skills"]:
            elements.append(
                Paragraph(
                    f"• {skill}",
                    styles["BodyText"]
                )
            )

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "<b>Suggestions</b>",
            styles["Heading2"]
        )
    )

    for suggestion in suggestions:
        elements.append(
            Paragraph(
                f"• {suggestion}",
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1,20))

    if ai_feedback:

        elements.append(
            Paragraph(
                "<b>AI Career Feedback</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                ai_feedback.replace("\n", "<br/>"),
                styles["BodyText"]
            )
        )

    if chart_path:

        elements.append(Spacer(1,20))

        elements.append(
            Image(chart_path, width=400, height=250)
        )

    doc.build(elements)

    return report_path