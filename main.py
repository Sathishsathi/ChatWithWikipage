from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from wiki_plaintext import wiki_page_answer
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app) 
port=3000
# Database connection

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='foss_hack'
    )
    return connection


@app.route('/post', methods=['POST'])
def add_user():
    data = request.get_json()
    # print(data.get("question"),'request')
    user_name = "<user-name>" #data.get('user_name')
    question = data.get('question')
    answer = wiki_page_answer(page_name=question)
    
    if not user_name or not question or not answer:
        return jsonify({"error": "user_name, question and answer are required"}), 400
    # else :
        # return jsonify({answer}),200

    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        insert_query = "INSERT INTO PROMPT_TABLE (user_name,question,answer) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_name,question,answer))
        connection.commit()

        return jsonify({"message": answer}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=port,debug=True)