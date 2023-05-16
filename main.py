from app import app, session
from flask import request, jsonify, redirect
from models import *
from schemas import *
from utils.convert_str_to_datetime import to_datetime


@app.route('/')
def main_page():
    return '<h1>Backend for GOITeens managemet system</h1>'


@app.route('/docs')
def documentation():
    return redirect('https://yaroslavs-organization-1.gitbook.io/docs/', 302)