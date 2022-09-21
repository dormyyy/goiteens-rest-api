from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import to_datetime


@app.route('/')
def main_page():
    return '<h1>Backend for GOITeens managemet system</h1>'
