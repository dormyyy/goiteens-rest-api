from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json
import backup


# groups table routers {
@app.route('/register_group', methods=['POST'])
def register_group():
    name = request.form['name']
    group = session.query(Group).filter_by(name=name).first()
    courses = session.query(Course).all()
    if group:
        return jsonify(message='This group already exist'), 409
    else:
        group_name = name
        group_course_id = request.form['course_id']
        group_timetable = request.form['timetable']
        try:
            group_course_id = int(group_course_id)
            if group_course_id in [i.id for i in courses]:
                group = Group(name=group_name, course_id=group_course_id, timetable=group_timetable)
                session.add(group)
                session.commit()
                group = session.query(Group).filter_by(name=name).first()
                data = group_schema.dump(group)
                try:
                    backup.backup()
                except:
                    print('', end='')
                return jsonify(data=data, message=f'Group {group.id} successfully registered'), 201
            else:
                return jsonify(message='Invalid course_id field.'), 404
        except:
            return jsonify(message='Invalid course_id field.'), 404

@app.route('/remove_group/<int:group_id>', methods=['DELETE'])
def remove_group(group_id: int):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        session.delete(group)
        session.commit()
        backup.backup()
        return jsonify(message=f'Group {group.id} successfully deleted'), 200
    else:
        return jsonify(message='This group does not exist'), 404


@app.route('/groups', methods=['GET'])
def get_groups():
    groups_list = session.query(Group).all()
    result = groups_schema.dump(groups_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/update_group/<int:group_id>', methods=['PUT'])
def update_group(group_id: int):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        for key in request.form:
            if key == 'name':
                group.name = request.form['name']
            elif key == 'course_id':
                group.course_id = request.form['course_id']
            elif key == 'timetable':
                group.timetable = request.form['timetable']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        group = session.query(Group).filter_by(id=group_id).first()
        data = group_schema.dump(group)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Group {group.id} successfully updated'), 202
    else:
        return jsonify(message='Group does not exist'), 404
# groups table routers }