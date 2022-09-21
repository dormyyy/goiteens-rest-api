import backup
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json

# results table routers {
@app.route('/register_result', methods=['POST'])
def register_result():
    name = request.form['name']
    test = session.query(Results).filter_by(name=name).first()
    if test:
        return jsonify(message='This result already exist'), 409
    else:
        result_name = name
        result_description = request.form['description']
        result_color = request.form['color']    
        result = Results(name=result_name, description=result_description, color=result_color)
        session.add(result)
        session.commit()
        test = session.query(Results).filter_by(name=name).first()
        data = result_schema.dump(test)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Result {result.id} successfully registered.'), 202


@app.route('/remove_result/<int:result_id>', methods=['DELETE'])
def remove_result(result_id: int):
    result = session.query(Results).filter_by(id=result_id).first()
    if result:
        session.delete(result)
        session.commit()
        return jsonify(message=f'Result {result.id} successfully deleted.'), 200
    else:
        return jsonify(message='This result does not exist.'), 404


@app.route('/results', methods=['GET'])
def get_results():
    results_list = session.query(Results).all()
    result = results_schema.dump(results_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/update_result/<int:result_id>', methods=['PUT'])
def update_results(result_id: int):
    result = session.query(Results).filter_by(id=result_id).first()
    if result:
        for key in request.form:
            if key == 'name':
                result.name = request.form['name']
            elif key == 'description':
                result.description = request.form['description']
            elif key == 'color':
                result.color = request.form['color']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        result = session.query(Results).filter_by(id=result_id).first()
        data = result_schema.dump(result)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Result {result.id} successfully updated.'), 202
    else:
        return jsonify(message='Result does not exist.'), 404
# results table routers }