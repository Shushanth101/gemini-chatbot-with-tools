import mysql.connector
from mysql.connector import Error
from google import genai
from google.genai import types
import os
import decimal
from dotenv import load_dotenv
from email.message import EmailMessage
from imap_tools import MailBox, AND
from datetime import date
import datetime
import smtplib
from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import requests




load_dotenv()

class MySQLClient:
    def __init__(self, user, password, database, host='localhost'):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            self.conn = None
            self.cursor = None
            print(f"Error connecting to MySQL: {e}")

    def run_query(self, query: str) -> str:
        if not self.cursor:
            return "No active database connection."
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return "Query executed successfully."
        except Error as e:
            return f"Error executing query: {e}"


    def fetch_query(self, query: str):
        if not self.cursor:
            return "No active database connection."
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return self.convert_decimals(results)
        except Error as e:
            return f"Error fetching query results: {e}"

    def describe_table(self, table: str):
        if not self.cursor:
            return "No active database connection."
        try:
            self.cursor.execute(f"DESC {table}")
            return self.cursor.fetchall()
        except Error as e:
            return f"Error describing table '{table}': {e}"

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("Database connection closed.")
        except Error as e:
            print(f"Error closing connection: {e}")

    def convert_decimals(self,data):
        if isinstance(data, list):
            return [self.convert_decimals(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(self.convert_decimals(item) for item in data)
        elif isinstance(data, dict):
            return {k: self.convert_decimals(v) for k, v in data.items()}
        elif isinstance(data, decimal.Decimal):
            return float(data)  # or str(data)
        else:
            return data


def google_search(query: str):
    client = genai.Client(api_key=os.environ.get("google_api_key_1"))
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                google_search=types.GoogleSearchRetrieval
            )]
        )
    )
    search_results = response.candidates[0].grounding_metadata.grounding_chunks
    data = [(chunk.web.title, chunk.web.uri) for chunk in search_results]
    return {"text_answer": response.text, "search_results_with_website_links_and_titles": data}


def read_mail(limit: int):
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
                    "date":  msg.date.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S'),
                    "subject": msg.subject,
                    "body": msg.text
                })
    except Exception as e:
        return f"Error connecting to the mailbox: {e}"

    return emails


def send_mail(recepient_email: str, subject: str, body: str) -> str:
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

# Type-safe version of read_mail_with_filters function
def read_mail_with_filters(from_date: str, to_date: str, email: str, *, subject: Optional[str] = None) -> List[Dict[str, str]]:
    EMAIL = os.getenv('EMAIL')
    APP_PASSWORD = os.getenv('APP_PASSWORD')

    if not EMAIL or not APP_PASSWORD:
        raise ValueError("Email and App Password must be set in environment variables")

    # Directly parse from_date and to_date strings to datetime objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    emails: List[Dict[str, str]] = []

    try:
        with MailBox('imap.gmail.com').login(EMAIL, APP_PASSWORD) as mailbox:
            # Build query with date filters and optional subject filter
            query = AND(from_=email, date_gte=date(from_date), date_lt=date(to_date))
            if subject:
                query = AND(query, subject=subject)

            # Fetch and process the matching messages
            for msg in mailbox.fetch(query):
                emails.append({
                    "from": msg.from_,
                    "to": msg.to,
                    "date": msg.date.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S'),
                    "subject": msg.subject,
                    "body": msg.text
                })
    except Exception as e:
        return f"Error connecting to the mailbox: {e}"

    return emails


def transcribe_yt_video(video_id:str)-> str:
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    full_text=""
    for snippet in fetched_transcript:
        full_text += snippet.text
    return full_text

def get_web_content(link:str)->str:
    base_url = "https://r.jina.ai"
    response = requests.get(base_url+"/"+link)
    if response.status_code == 200 :
        return response.text
    else :
        return "some error ocurred"




tool_client=MySQLClient("root","prodigy","store_db","localhost")
run_query = tool_client.run_query
fetch_query = tool_client.fetch_query
describe_table = tool_client.describe_table
close = tool_client.close

tools_list = [google_search,
            run_query,
            fetch_query,
            describe_table,
            close,
            read_mail,
            read_mail_with_filters,
            send_mail,
            transcribe_yt_video,
            get_web_content
            ]

if __name__=="__main__":
    print(send_mail("b23ai101@kitsw.ac.in","testing","test email"))