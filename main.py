from flask import Flask, jsonify, request, session
from flask_session import Session
import uuid
from wiki_service import get_page_content
from llm_service import get_response
from flask_cors import CORS
import os


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app) 
Session(app)
port=3000
# Database connection

def create_session(page_name):
    session_id = uuid.uuid4()
    session[session_id] = get_page_content(page_name)
    return session_id


@app.route('/<page_name>/<query>', methods=['GET', 'POST'])
def home(page_name, query):
    session_id = request.cookies.get('session_id', None)
    set_cookie = False
    if not session_id:
        set_cookie = True
        session_id = create_session(page_name)
    response = "dummy resp"
    if set_cookie:
        resp = jsonify({"success": response, "cookie": session_id})
    else:
        resp = jsonify({"success": response})
    return resp


# @app.route('/post', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     # print(data.get("question"),'request')
#     user_name = "<user-name>" #data.get('user_name')
#     question = data.get('question')
#     answer = wiki_page_answer(page_name=question)
    
#     if not user_name or not question or not answer:
#         return jsonify({"error": "user_name, question and answer are required"}), 400
#     # else :
#         # return jsonify({answer}),200

#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     try:
#         insert_query = "INSERT INTO PROMPT_TABLE (user_name,question,answer) VALUES (%s, %s, %s)"
#         cursor.execute(insert_query, (user_name,question,answer))
#         connection.commit()

#         return jsonify({"message": answer}), 201
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=port,debug=True)