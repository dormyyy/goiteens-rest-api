from email import message
from app import app, session
from flask import request, jsonify
from models import *
from schemas import * 

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
            description = request.form['description']
            login = request.form['login']
            password = request.form['password']
            manager = Manager(name=manager_name, description=description, login=login, password=password)
            session.add(manager)
            session.commit()
            test = session.query(Manager).filter_by(name=name).first()
            data = manager_schema.dump(test)
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
        return jsonify(message=f'Manager {manager.id} successfully deleted.'), 202
    else:
        return jsonify(message='Manager does not exist'), 404


@app.route('/managers', methods=['GET'])
def get_managers():
    managers_list = session.query(Manager).all()
    result = managers_schema.dump(managers_list)
    return jsonify(data=result)


# /manager/update/<int:manager_id>
@app.route('/update_manager/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        for key in request.form:
            if key == 'name':
                manager.name = request.form['name']
            elif key == 'description':
                manager.description = request.form['description']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        manager = session.query(Manager).filter_by(id=manager_id).first()
        data = manager_schema.dump(manager)
        return jsonify(data=data, message=f'Manager {manager.name} successfully updated'), 202
    else:
        return jsonify(message='This manager does not exist.'), 404