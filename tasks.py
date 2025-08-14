import os
import smtplib
from email.mime.text import MIMEText
from rq import get_current_job

# Add import for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def print_message(msg, extra):
    job = get_current_job()
    print(f"Worker says: {msg}")
    print(f"Extra info: {extra}")
    if job:
        print(f"My job ID is: {job.id}")

def send_email(recipient, subject, body):
    """
    Sends an email using SMTP. If using MailHog (default in docker-compose),
    emails are captured locally and can be viewed at http://localhost:8025.
    """
    job = get_current_job()
    print(f"Sending email to {recipient} (Job ID: {job.id if job else 'N/A'})")

    smtp_server = os.environ.get("SMTP_SERVER", "localhost")
    smtp_port = int(os.environ.get("SMTP_PORT", 1025))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    sender = os.environ.get("SMTP_SENDER", "anything@example.com")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() if smtp_port == 587 else None
            if smtp_user:
                server.login(smtp_user, smtp_password)
            server.sendmail(sender, [recipient], msg.as_string())
        print("Email sent! If using MailHog, check http://localhost:8025")
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_pdf_report(filename, content):
    """
    Generates a PDF report with the given content and saves it to disk.
    """
    job = get_current_job()
    print(f"Generating PDF report: {filename} (Job ID: {job.id if job else 'N/A'})")
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, content)
        c.save()
        print(f"PDF report saved as {filename}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")