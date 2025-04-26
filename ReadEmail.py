from imap_tools import MailBox, AND
from datetime import date

EMAIL = 'itsmeshus07@gmail.com'
APP_PASSWORD = 'rhwlvbbjfohnmhlx'

with MailBox('imap.gmail.com').login(EMAIL, APP_PASSWORD) as mailbox:
    # Get the last 3 emails from inbox (sorted newest first)
    messages = mailbox.fetch(reverse=True, limit=3)

    for msg in messages:
        print("="*50)
        print(f"From   : {msg.from_}")
        print(f"Date   : {msg.date}")
        print(f"Subject: {msg.subject}")
        print(f"Body   : {msg.text[:300]}")  # Preview first 300 characters


import os
from dotenv import load_dotenv
from imap_tools import MailBox

load_dotenv()
def read_mail(limit: int):
    # Validate that limit is a positive integer
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit should be a positive integer")


    EMAIL = os.getenv('EMAIL')
    APP_PASSWORD = os.getenv('APP_PASSWORD')

    if not EMAIL or not APP_PASSWORD:
        raise ValueError("Email and App Password must be set in environment variables")

    # Initialize the list to store emails
    emails = []

    try:
        with MailBox('imap.gmail.com').login(EMAIL, APP_PASSWORD) as mailbox:
            messages = mailbox.fetch(reverse=True, limit=limit)
            for msg in messages:
                emails.append({
                    "from": msg.from_,
                    "to": msg.to,
                    "date": msg.date,
                    "subject": msg.subject,
                    "body": msg.text
                })
    except Exception as e:
        raise ConnectionError(f"Error connecting to the mailbox: {e}")

    return emails


def read_mail_with_filters(from_date, to_date, email, *, subject=None):
    EMAIL = os.getenv('EMAIL')
    APP_PASSWORD = os.getenv('APP_PASSWORD')

    if not EMAIL or not APP_PASSWORD:
        raise ValueError("Email and App Password must be set in environment variables")

    emails = []

    try:
        with MailBox('imap.gmail.com').login(EMAIL, APP_PASSWORD) as mailbox:
            # Fetch emails with the provided filters
            query = AND(from_=email, date_gte=date(from_date), date_lt=date(to_date))
            if subject:
                query = AND(query, subject=subject)

            for msg in mailbox.fetch(query):
                emails.append({
                    "from": msg.from_,
                    "to": msg.to,
                    "date": msg.date,
                    "subject": msg.subject,
                    "body": msg.text
                })
    except Exception as e:
        return f"Error connecting to the mailbox: {e}"

    return emails
