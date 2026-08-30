import smtplib
import os
import logging
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def send_reset_email(to_email, reset_link):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)

    subject = "Reset your password"
    body = f"""Hi,

We received a request to reset your password.

Click the link below to set a new password (expires in 30 minutes):
{reset_link}

If you didn't request this, you can safely ignore this email.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, [to_email], msg.as_string())
