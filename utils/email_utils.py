import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables (recommended)
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")  # your Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")  # your App Password

def send_email(subject, to_email, content):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg.set_content(content)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
