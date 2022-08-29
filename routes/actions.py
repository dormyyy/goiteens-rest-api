from email import message
from utils.convert_str_to_datetime import str_to_datetime
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *


@app.route('/register_action', methods=['POST'])
def register_action():
    actor_role = request.form['actor_role']
    actor_id = request.form['actor_id']
    changing_table = request.form['table']
    query = request.form['query']
    datetime = request.form['datetime']
    datetime = str_to_datetime(datetime)
    role = session.query(Roles).filter_by(id=actor_role)
    user = session.query(Users).filter_by(id=actor_id)
    if role and user:
        action = Actions(actor_role=actor_role, actor_id=actor_id,
                         changing_table=changing_table, query=query, datetime=datetime)
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


#@app.route('/delete_actions', methods=['GET'])
#def actions():