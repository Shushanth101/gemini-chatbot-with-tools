import os
from email.message import EmailMessage
import smtplib

# Your details
your_email = "itsmeshus07@gmail.com"
app_password = "rhwlvbbjfohnmhlx"  # 16-character app password from Google
to_email = "b23ai101@kitsw.ac.in"

# Compose the email
msg = EmailMessage()
msg['Subject'] = "Test Email from Python"
msg['From'] = your_email
msg['To'] = to_email
msg.set_content("Hello, this is a test email sent using Python and Gmail App Password!")

# Send the email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(your_email, app_password)
        smtp.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print("Error:", e)


def send_mail(recepient_email, subject, body):
    EMAIL = os.getenv('EMAIL')
    APP_PASSWORD = os.getenv('APP_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = recepient_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e} "