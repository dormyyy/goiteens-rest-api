from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json
import backup


# courses table routers {
@app.route('/register_course', methods=['POST'])
def register_course():
    name = request.form['name']
    course = session.query(Course).filter_by(name=name).first()
    if course:
        return jsonify(message='This course already exist'), 409
    else:
        course_name = name
        course_description = request.form['description']
        course = Course(name=course_name, description=course_description)
        session.add(course)
        session.commit()
        course = session.query(Course).filter_by(name=name).first()
        data = course_schema.dump(course)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Course {course.id} successfully registered'), 201


@app.route('/remove_course/<int:course_id>', methods=['DELETE'])
def remove_course(course_id: int):
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        session.delete(course)
        session.commit()
        backup.backup()
        return jsonify(message=f'Course {course.id} successfully deleted'), 200
    else:
        return jsonify(message='Course does not exist'), 404


@app.route('/courses', methods=['GET'])
def get_courses():
    courses_list = session.query(Course).all()
    result = courses_schema.dump(courses_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)


@app.route('/update_course/<int:course_id>', methods=['PUT'])
def update_course(course_id: int):
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        for key in request.form:
            if key == 'name':
                course.name = request.form['name']
            elif key == 'description':
                course.description = request.form['description']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        course = session.query(Course).filter_by(id=course_id).first()
        data = course_schema.dump(course)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Course {course.id} successfully updated'), 202
    else:
        return jsonify(message='This course does not exist'), 404
# courses table routers }