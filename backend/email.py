from flask_mail import Message
from backend.extensions import mail

def send_email(recipient, subject, body):
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body
        )

        mail.send(msg)
        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:")
        print(e)


def send_html_email(recipient, subject, html):

    msg = Message(
        subject=subject,
        recipients=[recipient]
    )

    msg.html = html

    mail.send(msg)