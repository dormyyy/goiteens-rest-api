from datetime import timedelta
import ast
import json
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour


@app.route('/current_confirmation', methods=['GET'])
def get_current_confirmations():
    pass


