from typing import Tuple

from app import app, session
from flask import request, jsonify, Response
from models import *
from schemas import *
from utils.convert_str_to_datetime import to_datetime, get_current_date
from utils import data_to_json
import backup


@app.route('/week/register', methods=['POST'])
def register_week():
    try:
        week_start = to_datetime(request.form['date_start'])
        week_finish = to_datetime(request.form['date_finish'])
    except:
        return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404
    week = session.query(Weeks).filter_by(date_start=week_start).first()
    if week:
        return jsonify(message='This week already exist'), 409
    else:
        delta = (week_finish - week_start).days
        if delta != 6:
            return jsonify(message='Invalid dates. Week must includes 7 days'), 404
        else:
            week = Weeks(date_start=week_start, date_finish=week_finish)
            session.add(week)
            session.commit()
            week = session.query(Weeks).filter_by(date_start=week_start).first()
            data = week_schema.dump(week)
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(data=data, message=f'Week {week.id} successfully registered'), 201
    

@app.route('/week/remove/<int:week_id>', methods=['DELETE'])
def remove_week(week_id: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    if week:
        session.delete(week)
        session.commit()
        backup.backup()
        return jsonify(message=f'Week {week.id} successfully deleted'), 200
    else:
        return jsonify(message='Week does not exist'), 404


@app.route('/weeks', methods=['GET'])
def get_weeks():
    weeks_list = session.query(Weeks).all()
    result = weeks_schema.dump(weeks_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/active_week_id', methods=['GET'])
def get_active_week_id():
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
            backup.backup()
            return jsonify(week_id=current_week_id)


@app.route('/get_week_id/<string:date>', methods=['GET'])
def get_week_id(date: str) -> tuple[Response, int]:
    try:
        weeks = session.query(Weeks).all()
        current_date = to_datetime(date).date()
        for i in [i.date_start for i in weeks]:
            if 0 <= (current_date - i).days <= 7:
                week = session.query(Weeks).filter_by(date_start=i).first()
        result = week_schema.dump(week)
        return jsonify(result), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
