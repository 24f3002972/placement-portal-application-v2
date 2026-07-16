import os
import pandas as pd
from backend.utils.email import send_email
from backend.models import Student
from backend.extensions import celery
from backend.models import Application
from datetime import datetime, timedelta
from backend.models import Drive, Student
from backend.utils.email import send_email, send_html_email

@celery.task
def export_student_applications(student_id):

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    rows = []

    for application in applications:

        rows.append({

            "Student ID": application.student.id,

            "Company Name": application.drive.company.company_name,

            "Drive Title": application.drive.job_title,

            "Application Status": application.status,

            "Date": application.date.strftime("%d-%m-%Y")

        })

    export_folder = os.path.join("backend", "exports")

    os.makedirs(export_folder, exist_ok=True)

    filename = os.path.join(
        export_folder,
        f"student_{student_id}.csv"
    )

    df = pd.DataFrame(rows)

    df.to_csv(filename, index=False)
    student = Student.query.get(student_id)

    send_email(

        student.user.email,

        "CSV Export Completed",

        f"""
    Hello {student.user.name},

    Your placement application history has been exported successfully.

    File Location:

    {filename}

    Regards,
    Placement Portal
    """

    )
    return filename

@celery.task
def send_daily_reminders():

    today = datetime.now()

    limit = today + timedelta(days=2)

    drives = Drive.query.filter(
        Drive.status == "Approved"
    ).all()
    for drive in drives:
        if today <= drive.deadline <= limit:

            students = Student.query.filter_by(
                branch=drive.eligible_branch,
                year=drive.eligible_year
            ).all()

            for student in students:
                if student.cgpa >= drive.minimum_cgpa:
                    print(f"Sending email to: {student.user.email}")
                    send_email(

                        student.user.email,

                        "Placement Reminder",

                        f"""
Hello {student.user.name},

Reminder!

The placement drive

{drive.job_title}

will close on

{drive.deadline.strftime("%d-%m-%Y")}.

Please apply before the deadline.

Regards,
Placement Cell
"""
                    )

    return "Daily reminders sent."

@celery.task
def send_monthly_report():

    total_drives = Drive.query.count()

    total_applications = Application.query.count()

    total_selected = (
        Application.query
        .filter_by(status="Selected")
        .count()
    )

    html = f"""
    <html>

    <head>

        <style>

            body {{
                font-family: Arial;
                padding:20px;
            }}

            table {{
                width:60%;
                border-collapse:collapse;
            }}

            th {{
                background:#0d6efd;
                color:white;
            }}

            th, td {{
                border:1px solid #ccc;
                padding:10px;
            }}

        </style>

    </head>

    <body>

        <h2>Monthly Placement Activity Report</h2>

        <p>
            Generated on
            {datetime.now().strftime("%d-%m-%Y")}
        </p>

        <table>

            <tr>

                <th>Metric</th>

                <th>Value</th>

            </tr>

            <tr>

                <td>Total Drives Conducted</td>

                <td>{total_drives}</td>

            </tr>

            <tr>

                <td>Total Applications</td>

                <td>{total_applications}</td>

            </tr>

            <tr>

                <td>Total Selected Students</td>

                <td>{total_selected}</td>

            </tr>

        </table>

    </body>

    </html>
    """

    admin_email = "24f3002972@ds.study.iitm.ac.in"

    send_html_email(

        admin_email,

        "Monthly Placement Activity Report",

        html

    )

    return "Monthly report sent."
