import backup
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json


# roles table routers {
@app.route('/register_role', methods=['POST'])
def register_role():
    name = request.form['name']
    test = session.query(Roles).filter_by(name=name).first()
    if test:
        return jsonify(message='This role already exist'), 409
    else:
        role_name = name
        role_description = request.form['description']
        role = Roles(name=role_name, description=role_description)
        session.add(role)
        session.commit()
        test = session.query(Roles).filter_by(name=name).first()
        data = role_schema.dump(test)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Role {role.id} successfully registered'), 202


@app.route('/remove_role/<int:role_id>', methods=['DELETE'])
def remove_role(role_id: int):
    role = session.query(Roles).filter_by(id=role_id).first()
    if role:
        session.delete(role)
        session.commit()
        return jsonify(message=f'Role {role.id} successfully deleted.'), 200
    else:
        return jsonify(message='This role does not exist'), 404


@app.route('/roles', methods=['GET'])
def get_roles():
    roles_list = session.query(Roles).all()
    result = roles_schema.dump(roles_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/update_role/<int:role_id>', methods=['PUT'])
def update_role(role_id: int):
    role = session.query(Roles).filter_by(id=role_id).first()
    if role:
        for key in request.form:
            if key == 'name':
                role.name = request.form['name']
            elif key == 'description':
                role.description = request.form['desctiption']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        role = session.query(Roles).filter_by(id=role_id).first()
        data = role_schema.dump(role)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Role {role.id} successfully updated.'), 202
    else:
        return jsonify(message='Role does not exist'), 404
# roles table routers }