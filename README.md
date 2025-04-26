# gemini-chatbot-with-tools
A practical project showing how to build essential tools (like email integration, SQL operations, web search, YouTube transcripts) for AI agents — not just the agent itself.

# 💬 Gemini 2.0 Flash Chatbot (with Real-World Tool Integration)

This project is a console-based chatbot powered by Google's Gemini 2.0 Flash model.  
It integrates various tools like MySQL database operations, Google Search, Email operations, YouTube transcript extraction, and Web content fetching, enhancing the chat experience with real-world functionalities.

---

## 🛠 Tech Stack
- Python
- Google GenAI SDK (`google.generativeai`)
- MySQL
- SMTP & IMAP for Email
- REST APIs (YouTube Transcript API, Web Content API)
- dotenv

---

## 📂 Project Structure

| File | Description |
|:-----|:------------|
| `main.py` | Initializes the chatbot and handles user interaction. |
| `tools.py` | Collection of utility functions and database/email/YouTube tools. |
| `store_to_db.py` | Stores chat history into a MySQL database (`chats` database). |

---

## ⚙️ Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/Shushanth101/gemini-chatbot-with-tools.git
cd gemini-chatbot-with-tools
```

### 2. Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file with the following variables:
```ini
google_api_key_1=YOUR_GEMINI_API_KEY (get your gemini api key here ==> https://aistudio.google.com/app/apikey
EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password (setup your app password in gmail)
```

### 4. Set up MySQL databases:

- `store_db` for running SQL queries.
- `chats` database with a `chat_log` table:
```sql
CREATE DATABASE chats;
USE chats;
CREATE TABLE chat_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(255),
    content TEXT
);
```

---

## 🧩 Features

- 💬 Chat with Gemini 2.0 Flash Model
- 🔎 Google Search Retrieval
- 📧 Send and Read Emails
- 📝 Run SQL Queries on Local MySQL Database
- 🎥 Fetch YouTube Video Transcripts
- 🌐 Fetch Web Content
- 🗄️ Store Chat History into MySQL

---

## 🚀 How to Run
```bash
python main.py
```
- Start chatting!
- Type `e` or `exit` to end the session.

---

## 🙏 Acknowledgements

- Google GenAI
- YouTube Transcript API
- Jina.ai Web Reader API
---
Everyone talks about agents. This project teaches you how to actually build the real-world tools that make agents powerful — like reading emails, sending emails, running SQL queries, fetching YouTube transcripts, and more.

