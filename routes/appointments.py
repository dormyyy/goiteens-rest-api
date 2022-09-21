from email import message
from utils import data_to_json
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
import backup


# appointments table routers {
@app.route('/register_appointment', methods=['POST'])
def register_appointment():
    appointment_slot_id = request.form['slot_id']
    test = session.query(Appointment).filter_by(slot_id=appointment_slot_id).first()
    slots = session.query(Slots).all()
    courses = session.query(Course).all()
    if test:
        return jsonify(message='This appointment already exist'), 409
    else:
        appointment_age = request.form['age']
        appointment_zoho_link = request.form['zoho_link']
        appointment_course_id = request.form['course_id']
        appointment_comments = request.form['comments']
        appointment_group_id = request.form['group_id']
        appointment_phone = request.form['phone']
        if int(appointment_slot_id) in [i.id for i in slots] and int(appointment_course_id) in [i.id for i in courses]:
            appointment = Appointment(age=appointment_age, zoho_link=appointment_zoho_link,
            slot_id=appointment_slot_id, course_id=appointment_course_id, comments=appointment_comments, group_id=appointment_group_id, phone=appointment_phone)
            session.add(appointment)
            session.commit()
            test = session.query(Appointment).filter_by(slot_id=appointment_slot_id).first()
            data = appointment_schema.dump(test)
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(data=data, message=f'Appointment {appointment.id} successfully registered'), 201
        else:
            return jsonify(message='Invalid field course_id or slot_id'), 409


@app.route('/remove_appointment/<int:appointment_id>', methods=['DELETE'])
def remove_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        backup.backup()
        return jsonify(message=f'Appointment {appointment.id} successfully deleted.'), 200
    else:
        return jsonify(message='This appointment does not exist.'), 404


@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments_list = session.query(Appointment).all()
    result = appointments_schema.dump(appointments_list)
    try:
        backup.backup()
    except:
        print('', end='')
    backup.backup()
    return jsonify(data=result)


@app.route('/update_appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        for key in request.form:
            if key == 'age':
                appointment.age = request.form['age']
            elif key == 'zoho_link':
                appointment.zoho_link = request.form['zoho_link']
            elif key == 'slot_id':
                appointment.slot_id = request.form['slot_id']
            elif key == 'course_id':
                appointment.course_id = request.form['course_id']
            elif key == 'comments':
                appointment.comments = request.form['comments']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        appointment = session.query(Appointment).filter_by(id=appointment_id).first()
        data = appointment_schema.dump(appointment)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Appointment {appointment.id} successfully updated.'), 202
    else:
        return jsonify(message='Appointment does not exist'), 404
# appointments table routers }


@app.route('/appointment/<int:slot_id>', methods=['GET'])
def get_appointment_by_slot(slot_id: int):
    appointment = session.query(Appointment).filter_by(slot_id=slot_id).first()
    if appointment:
        result = appointment_schema.dump(appointment)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=result), 200
    else:
        return jsonify(message='Appointment does not exist'), 404