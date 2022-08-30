from email import message
from utils.convert_str_to_datetime import str_to_datetime, get_current_date
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from datetime import datetime


@app.route('/register_action', methods=['POST'])
def register_action():
    actor_role = request.form['actor_role']
    actor_id = request.form['actor_id']
    changing_table = request.form['changing_table']
    query = request.form['query']
    date_time = str(datetime.now()).split()
    date = date_time[0].split('-')
    date_time = f'{date[2]}.{date[1]}.{date[0]} {date_time[1].split(".")[0]}'
    date_time = str_to_datetime(date_time)
    role = session.query(Roles).filter_by(id=actor_role)
    user = session.query(Users).filter_by(id=actor_id)
    if role and user:
        action = Actions(actor_role=actor_role, actor_id=actor_id,
                         changing_table=changing_table, query=query, datetime=date_time)
        session.add(action)
        session.commit()
        data = action_schema.dump(action)
        return jsonify(data=data, message='Successfully created'), 202
    else:
        return jsonify(message='User or role not found'), 404


@app.route('/actions', methods=['GET'])
def actions():
    actions = session.query(Actions).all()
    data = []
    for i in actions:
        data.append(action_schema.dump(i))
    return jsonify(data=data), 202


@app.route('/delete_actions', methods=['DELETE'])
def delete_actions():
    actions = session.query(Actions).all()
    today = get_current_date()
    for action in actions:
        if (datetime.strptime(str(today), "%Y-%m-%d") - datetime.strptime(str(action.datetime).split()[0], "%Y-%m-%d")).days > 2:
            session.delete(action)
            session.commit()
    return jsonify(message='Successfully'), 200
