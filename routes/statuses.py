import backup
from app import app, ma, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json

# status table routers {
@app.route('/register_status', methods=['POST'])
def register_status():
    name = request.form['name']
    status = session.query(Status).filter_by(name=name).first()
    if status:
        return jsonify(message='This status already exist'), 409
    else:
        status_name = name
        status_color = request.form['color']
        status = Status(name=status_name, color=status_color)
        session.add(status)
        session.commit()
        status = session.query(Status).filter_by(name=name).first()
        data = status_schema.dump(status)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Status {status.id} successfully registered'), 201


@app.route('/remove_status/<int:status_id>', methods=['DELETE'])
def remove_status(status_id: int):
    status = session.query(Status).filter_by(id=status_id).first()
    if status:
        session.delete(status)
        session.commit()
        backup.backup()
        return jsonify(message=f'Status {status.name} successfully deleted'), 202
    else:
        return jsonify(message='Status does not exist'), 404


@app.route('/statuses', methods=['GET'])
def get_statuses():
    statuses_list = session.query(Status).all()
    result = statuses_schema.dump(statuses_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/update_status/<int:status_id>', methods=['PUT'])
def update_status(status_id: int):
    status = session.query(Status).filter_by(id=status_id).first()
    if status:
        for key in request.form:
            if key == 'name':
                status.name = request.form['name']
            elif key == 'color':
                status.color = request.form['color']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        status = session.query(Status).filter_by(id=status_id).first()
        data = status_schema.dump(status)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Status {status.id} successfully updated'), 202
    else:
        return jsonify(message='This status does not exist.'), 404
# status table routers}