from app import app, session
from flask import request, jsonify
from models import *
from schemas import * 


# /user/register
@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    test = session.query(Users).filter_by(name=name).first()
    roles = session.query(Roles).all()
    if test:
        return jsonify(message='This user already exist'), 409
    else:
        user_name = name
        user_description = request.form['description']
        user_login = request.form['login']
        user_password = request.form['password']
        user_role_id = request.form['role_id']
        if int(user_role_id) in [i.id for i in roles]:
            user = Users(name=user_name, description=user_description,
            login=user_login, password=user_password, role_id=user_role_id)
            session.add(user)
            session.commit()
            test = session.query(Users).filter_by(name=name).first()
            data = user_schema.dump(test)
            return jsonify(data=data, message=f'User {user.id} successfully registered'), 202
        else:
            return jsonify(message='Invalid role_id field'), 404

# /user/remove
@app.route('/remove_user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id: int):
    user = session.query(Users).filter_by(id=user_id).first()
    if not user:
        return jsonify(message='This user does not exist'), 404
    session.delete(user)
    session.commit()
    return jsonify(message=f'User {user.id} successfully deleted.'), 200

        
@app.route('/users', methods=['GET'])
def get_users():
    users_list = session.query(Users).all()
    result = users_schema.dump(users_list)
    return jsonify(data=result)

# /user/update/<int:user_id>
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    user = session.query(Users).filter_by(id=user_id).first()
    if not user:
        return jsonify(message='User does not exist'), 404
 
    for key in request.form:
        if key == 'name':
            user.name = request.form['name']
        elif key == 'description':
            user.description = request.form['description']
        elif key == 'login':
            user.login = request.form['login']
        elif key == 'password':
            user.login = request.form['password']
        elif key == 'role_id':
            user.role_id = request.form['role_id']
        else:
            return jsonify(message=f'Invalid field {key}'), 404
    session.commit()
    user = session.query(Users).filter_by(id=user_id).first()
    data = user_schema.dump(user)
    return jsonify(data=data, message=f'User {user.id} successfully updated.'), 202

        
# users table routers }


# get user by id {
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = session.query(Users).filter_by(id=user_id).first()
    if not user:
        return jsonify(message='This user does not exist.'), 404
    result = user_schema.dump(user)
    return jsonify(data=result), 200

        
# get user by id}

# get users by role {
@app.route('/users/<string:role_name>', methods=['GET'])
def get_users_by_role(role_name: str):
    users_list = session.query(Users).filter_by(role_id=session.query(Roles).filter_by(name=role_name).first().id)
    result = users_schema.dump(users_list)
    return jsonify(data=result)
# get users by role }