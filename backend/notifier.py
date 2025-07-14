# notifier.py
# send_sms(phone_number, message) → uses Twilio or SMS API

# send_email(email_address, message) → optional

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body):
    sender_email = "jbsalas05@gmail.com"
    sender_password = "" #Insert code password here. 

    # Create the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())


# Example usage:
send_email("jbsalas05@gmail.com", "Seats Available!", "Quick! Your class now has open seats!")