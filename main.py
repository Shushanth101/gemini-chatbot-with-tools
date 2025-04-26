import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import tools_list
from system_instruction import system_instruction
from store_to_db import store_to_chat_log

load_dotenv()

GOOGLE_API_KEY = os.environ.get("google_api_key_1")
client = genai.Client(api_key=GOOGLE_API_KEY)

model_config = types.GenerateContentConfig(
    system_instruction=system_instruction,
    tools=tools_list
)

chat = client.chats.create(model="gemini-2.0-flash",config=model_config,history=[])

while(True):
    query=input(">>")
    if query in ('e','exit','E',"EXIT"):
        break
    response = chat.send_message(query)
    print()
    print("🤖 :",response.text)
    print(50*"==")

store_to_chat_log(chat.get_history())




