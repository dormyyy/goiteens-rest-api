import backup
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json

# /manager/register
@app.route('/register_manager', methods=['POST'])
def create_manager():
    name = request.form['name']
    test = session.query(Manager).filter_by(name=name).first()
    if test:
        return jsonify(message='This manager already exist'), 409
    else:
        try:
            manager_name = request.form['name']
            telegram = request.form['telegram']
            login = request.form['login']
            password = request.form['password']
            manager = Manager(name=manager_name, telegram=telegram, login=login, password=password)
            session.add(manager)
            session.commit()
            test = session.query(Manager).filter_by(name=name).first()
            data = manager_schema.dump(test)
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(data=data, message=f'Manager {manager.id} successfully registered'), 201
        except:
            return jsonify(message='Perhaps you forgot one of required fields'), 409


# /manager/remove/<int:manager_id>
@app.route('/remove_manager/<int:manager_id>', methods=['DELETE'])
def remove_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        session.delete(manager)
        session.commit()
        backup.backup()
        return jsonify(message=f'Manager {manager.id} successfully deleted.'), 202
    else:
        return jsonify(message='Manager does not exist'), 404


@app.route('/managers', methods=['GET'])
def get_managers():
    managers_list = session.query(Manager).all()
    result = managers_schema.dump(managers_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


# /manager/update/<int:manager_id>
@app.route('/update_manager/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        for key in request.form:
            if key == 'name':
                manager.name = request.form['name']
            elif key == 'telegram':
                manager.telegram = request.form['telegram']
            elif key == 'login':
                manager.login = request.form['login']
            elif key == 'password':
                manager.password = request.form['password']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        manager = session.query(Manager).filter_by(id=manager_id).first()
        data = manager_schema.dump(manager)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Manager {manager.name} successfully updated'), 202
    else:
        return jsonify(message='This manager does not exist.'), 404


@app.route('/manager/<string:manager_name>', methods=['GET'])
def get_manager_by_name(manager_name: str):
    manager = session.query(Manager).filter_by(name=manager_name).first()
    if manager:
        result = manager_schema.dump(manager)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=result), 200
    else:
        return jsonify(message='Manager does not exists'), 404