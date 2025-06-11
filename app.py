from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from config import DATABASE_URI

app = Flask(__name__)

engine = create_engine(DATABASE_URI)

if __name__ == '__main__':
    app.run(port=5050, debug=True)