import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body):
    # Get credentials from environment variables
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    # Check if credentials are available
    if not sender_email or not sender_password:
        raise ValueError("Email credentials not found. Please set SENDER_EMAIL and SENDER_PASSWORD environment variables.")
    
    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"✅ Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        raise e