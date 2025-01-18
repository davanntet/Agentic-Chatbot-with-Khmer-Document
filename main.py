from flask import Flask, jsonify,request
from agentic_ai import AgenticAI
from agentic_data_pipline import AgenticDataPipline
import time
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)
model =  AgenticAI()
preccssing = AgenticDataPipline()
@app.route('/')
def home():
    return jsonify(message="Welcome to AMK Agentic AI API!")

@app.route('/agent', methods=['GET'])
def agent():
    question = request.args.get('question')
    answers = model.ask_question(question)
    return jsonify(answers=answers)

@app.route('/search', methods=['GET'])
def search():
    question = request.args.get('question')
    related_docs = model.get_similar_documents(question)
    return jsonify(related_docs=related_docs.tolist())

#multi files upload
@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    for file in files:
        file_name = str(time.time())+"_"+file.filename
        file.save(str(os.environ.get('DATA_SOURCE_PATH'))+"/"+file_name)
        preccssing.single_precessing(file_name)
    return jsonify(message="Files uploaded successfully")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)