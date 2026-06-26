from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

import os
from datetime import datetime


def generate_pdf_report(
        interview_type,
        interview_duration,
        eye_score,
        head_score,
        posture_score,
        communication_score,
        confidence_score,
        asked_questions,
        feedback,
):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/report_{timestamp}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "<b><font size=20>AI Interview Coach</font></b>",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 0.3 * inch))

    subtitle = Paragraph(
        "<b>Interview Performance Report</b>",
        styles["Heading2"]
    )

    story.append(subtitle)
    story.append(Spacer(1, 0.2 * inch))

    info = [
        ["Interview Type", interview_type],
        ["Interview Duration", f"{interview_duration} sec"],
        ["Date", datetime.now().strftime("%d %B %Y %I:%M %p")]
    ]

    table = Table(info)

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold")

    ]))

    story.append(table)

    story.append(Spacer(1,0.3*inch))

    scores = [

        ["Metric","Score"],

        ["Eye Contact",f"{eye_score}%"],

        ["Head Stability",f"{head_score}%"],

        ["Posture",f"{posture_score}%"],

        ["Communication",f"{communication_score}%"],

        ["Confidence",f"{confidence_score}%"]

    ]

    score_table = Table(scores)

    score_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    story.append(score_table)

    story.append(Spacer(1,0.3*inch))

    story.append(

        Paragraph(
            "<b>Interview Questions</b>",
            styles["Heading2"]
        )
    )

    for q in asked_questions:

        story.append(

            Paragraph(
                f"• {q}",
                styles["BodyText"]
            )

        )

    story.append(Spacer(1,0.25*inch))

    story.append(

        Paragraph(
            "<b>Personalized Feedback</b>",
            styles["Heading2"]
        )

    )

    for line in feedback:

        story.append(

            Paragraph(
                f"• {line}",
                styles["BodyText"]
            )

        )

    story.append(Spacer(1,0.25*inch))

    if confidence_score >= 85:

        rating = "★★★★★ Excellent"

    elif confidence_score >= 70:

        rating = "★★★★☆ Good"

    elif confidence_score >= 50:

        rating = "★★★☆☆ Average"

    else:

        rating = "★★☆☆☆ Needs Improvement"

    story.append(

        Paragraph(
            f"<b>Overall Rating : {rating}</b>",
            styles["Heading2"]
        )

    )

    doc.build(story)

    print(f"PDF Report saved : {filename}")