import mysql.connector

def store_to_chat_log(history):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="prodigy",
            database="chats"
        )
        cursor = conn.cursor()

        for i in range(0, len(history)):
            query = "INSERT INTO chat_log(role, content) VALUES (%s, %s)"
            cursor.execute(query, (history[i].role, history[i].parts[0].text))

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
