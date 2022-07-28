from app import app, session
from flask import request, jsonify
from models import *
from schemas import *

# appointments table routers {
@app.route('/register_appointment', methods=['POST'])
def register_appointment():
    name = request.form['name']
    test = session.query(Appointment).filter_by(name=name).first()
    slots = session.query(Slots).all()
    courses = session.query(Course).all()
    if test:
        return jsonify(message='This appointment already exist'), 409
    else:
        appointment_name = name
        appointment_zoho_link = request.form['zoho_link']
        appointment_slot_id = request.form['slot_id']
        appointment_course_id = request.form['course_id']
        appointment_comments = request.form['comments']
        if int(appointment_slot_id) in [i.id for i in slots] and int(appointment_course_id) in [i.id for i in courses]:
            appointment = Appointment(name=appointment_name, zoho_link=appointment_zoho_link,
            slot_id=appointment_slot_id, course_id=appointment_course_id, comments=appointment_comments)
            session.add(appointment)
            session.commit()
            test = session.query(Appointment).filter_by(name=name).first()
            data = appointment_schema.dump(test)
            return jsonify(data=data, message=f'Appointment {appointment.id} successfully registered'), 202
        else:
            return jsonify(message='Invalid field course_id or slot_id')


@app.route('/remove_appointment/<int:appointment_id>', methods=['DELETE'])
def remove_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        return jsonify(message=f'Appointment {appointment.id} successfully deleted.'), 200
    else:
        return jsonify(message='This appointment does not exist.'), 404


@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments_list = session.query(Appointment).all()
    result = appointments_schema.dump(appointments_list)
    return jsonify(data=result)


@app.route('/update_appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        for key in request.form:
            if key == 'name':
                appointment.name = request.form['name']
            elif key == 'zoho_link':
                appointment.zoho_link = request.form['zoho_link']
            elif key == 'zlot_id':
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
        return jsonify(data=data, message=f'Appointment {appointment.id} successfully updated.'), 202
    else:
        return jsonify(message='Appointment does not exist'), 404
# appointments table routers }