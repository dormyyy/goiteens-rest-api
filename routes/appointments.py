from email import message
from utils import data_to_json
from app import app, session
from flask import Response, request, jsonify
from models import *
from schemas import *
import backup
from utils.convert_str_to_datetime import to_datetime

# Додаємо лог.
# Додаємо перевірку - чи є інший слот із цим менеджером і на цей час.
# appointments table routers {


@app.route('/register_appointment', methods=['POST'])
def register_appointment():
    appointment_slot_id = request.form['slot_id']
    test = session.query(Appointment).filter_by(
        slot_id=appointment_slot_id).first()
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
            test = session.query(Appointment).filter_by(
                slot_id=appointment_slot_id).first()
            data = appointment_schema.dump(test)
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(data=data, message=f'Appointment {appointment.id} successfully registered'), 201
        else:
            return jsonify(message='Invalid field course_id or slot_id'), 409

# Додаємо лог.


@app.route('/remove_appointment/<int:appointment_id>', methods=['DELETE'])
def remove_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(
        id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        backup.backup()
        return jsonify(message=f'Appointment {appointment.id} successfully deleted.'), 200
    else:
        return jsonify(message='This appointment does not exist.'), 404

# Додаємо перевірку - 1 appointment на 1 слот.


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

# Додаємо перевірку - 1 appointment на 1 слот.


@app.route('/update_appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(
        id=appointment_id).first()
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
        appointment = session.query(Appointment).filter_by(
            id=appointment_id).first()
        data = appointment_schema.dump(appointment)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Appointment {appointment.id} successfully updated.'), 202
    else:
        return jsonify(message='Appointment does not exist'), 404
# appointments table routers }

# Додаємо перевірку - 1 appointment на 1 слот.


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


@app.route('/get-current-meetings', methods=['GET'])
def get_current_meetings():
    try:
        try:
            date = to_datetime(request.form['date'])
        except:
            return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 400
        time = request.form.get('time', None)
        managers_list = request.form.get('managers_list', None)

        if managers_list:
            meetings_by_managers = session.query(Slots).filter(
                Slots.manager_id.in_([int(i) for i in managers_list.split(',')])).all()

        meetings = session.query(Appointment).filter(Appointment.slot_id.in_(
            [i.id for i in session.query(Slots).filter_by(date=date).all()])).all()
        if not time:
            if not managers_list:
                result = []
                for i in meetings:
                    try:
                        status = session.query(Slots).filter_by(
                            id=i.slot_id).first().status_id
                    except:
                        status = None
                    result.append(
                            {
                                'appointment_id': i.id,
                                'slot_id': i.slot_id,
                                'zoho_link': i.zoho_link,
                                'course_id': i.course_id,
                                'comments': i.comments,
                                'phone': i.phone,
                                'cancel_type': i.cancel_type,
                                'group_id': i.group_id,
                                'appointment_status': status    
                            })
                if not result:
                    return jsonify(message='Any appointments was not found.'), 404
                return jsonify(result), 200
            else:
                result = []
                for i in meetings:
                    if i.slot_id in [i.id for i in meetings_by_managers]:
                        try:
                            status = session.query(Slots).filter_by(
                                id=i.slot_id).first().status_id
                        except:
                            status = None
                        result.append(
                            {
                                'appointment_id': i.id,
                                'slot_id': i.slot_id,
                                'zoho_link': i.zoho_link,
                                'course_id': i.course_id,
                                'comments': i.comments,
                                'phone': i.phone,
                                'cancel_type': i.cancel_type,
                                'group_id': i.group_id,
                                'appointment_status': status    
                            })
                if not result:
                    return jsonify(message='Any appointments was not found.'), 404
                return jsonify(result), 200
        else:
            meetings_on_time = session.query(Appointment).filter(Appointment.slot_id.in_(
                [i.id for i in session.query(Slots).filter_by(date=date, time=time).all()])).all()
            if not managers_list:
                result = []
                for i in meetings_on_time:
                    try:
                        status = session.query(Slots).filter_by(
                            id=i.slot_id).first().status_id
                    except:
                        status = None
                    result.append(
                            {
                                'appointment_id': i.id,
                                'slot_id': i.slot_id,
                                'zoho_link': i.zoho_link,
                                'course_id': i.course_id,
                                'comments': i.comments,
                                'phone': i.phone,
                                'cancel_type': i.cancel_type,
                                'group_id': i.group_id,
                                'appointment_status': status    
                            })
                if not result:
                    return jsonify(message='Any appointments was not found.'), 404
                return jsonify(result), 200
            else:
                result = []
                for i in meetings_on_time:
                    if i.slot_id in [i.id for i in meetings_by_managers]:
                        try:
                            status = session.query(Slots).filter_by(
                                id=i.slot_id).first().status_id
                        except:
                            status = None
                        result.append(
                            {
                                'appointment_id': i.id,
                                'slot_id': i.slot_id,
                                'zoho_link': i.zoho_link,
                                'course_id': i.course_id,
                                'comments': i.comments,
                                'phone': i.phone,
                                'cancel_type': i.cancel_type,
                                'group_id': i.group_id,
                                'appointment_status': status    
                            }
                        )
                if not result:
                    return jsonify(message='Any appointments was not found.'), 404
                return jsonify(result), 200

    except Exception as e:
        session.rollback()
        return jsonify(error=str(e)), 400


@app.route('/get-current-appointments/<string:date>')
def get_current_appointments(date: str) -> Response:
    try:
        try:
            date = to_datetime(date)
        except:
            return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 400
        time = request.form.get('time', None)
        managers_list = request.form.get('managers_list', None)
        managers_ids = [i.id for i in session.query(Manager).all()]
        result = []
        if not time:
            if not managers_list:
                for manager_id in managers_ids:
                    manager_result = {
                    "manager_appointments": []
                    }
                    manager_result["manager_id"] = manager_id
                    manager_result["manager_name"] = session.query(Manager).filter_by(id=manager_id).first().name
                    for i in range(8, 23):
                        slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).first()
                        if not slot:
                            manager_result["manager_appointments"].append({
                                "time": i,
                                "slot_id": 0,
                                "status_id": 0
                            })
                        else:
                            appointment = session.query(Appointment).filter_by(slot_id=slot.id).first()
                            if appointment:
                                manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": appointment.id,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": appointment.cancel_type,
                                        "comments": appointment.comments,
                                        "course_id": appointment.course_id,
                                        "group_id": appointment.group_id,
                                        "phone": appointment.phone,
                                        "slot_id": slot.id,
                                        "zoho_link": appointment.zoho_link
                                    }
                                )
                            else:
                                manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": None,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": None,
                                        "comments": None,
                                        "course_id": None,
                                        "group_id": None,
                                        "phone": None,
                                        "slot_id": slot.id,
                                        "zoho_link": None
                                    }
                                )
                    result.append(manager_result)
            else:
                managers_ids = [int(i) for i in managers_list.split(', ')]
                for manager_id in managers_ids:
                    if not session.query(Manager).filter_by(id=manager_id).first():
                        return jsonify(message=f'Manager with id {manager_id} does not exist.'), 404
                    manager_result = {
                    "manager_appointments": []
                    }
                    manager_result["manager_id"] = manager_id
                    manager_result["manager_name"] = session.query(Manager).filter_by(id=manager_id).first().name
                    for i in range(8, 23):
                        slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).first()
                        if not slot:
                            manager_result["manager_appointments"].append(
                                {
                                    "time": i,
                                    "slot_id": 0,
                                    "status_id": 0
                                }
                            )
                        else:
                            appointment = session.query(Appointment).filter_by(slot_id=slot.id).first()
                            if appointment:
                                manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": appointment.id,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": appointment.cancel_type,
                                        "comments": appointment.comments,
                                        "course_id": appointment.course_id,
                                        "group_id": appointment.group_id,
                                        "phone": appointment.phone,
                                        "slot_id": slot.id,
                                        "zoho_link": appointment.zoho_link
                                    }
                                )
                            else:
                                manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": None,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": None,
                                        "comments": None,
                                        "course_id": None,
                                        "group_id": None,
                                        "phone": None,
                                        "slot_id": slot.id,
                                        "zoho_link": None
                                    }
                                )
                    result.append(manager_result)
        else:
            if not managers_list:
                for manager_id in managers_ids:
                    manager_result = {
                        "manager_appointments": []
                    }
                    manager_result["manager_id"] = manager_id
                    manager_result["manager_name"] = session.query(Manager).filter_by(id=manager_id).first().name
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=time).first()
                    if not slot:
                        manager_result["manager_appointments"].append(
                                {
                                    "time": time,
                                    "slot_id": 0,
                                    "status_id": 0
                                }
                        )
                    else:
                        appointment = session.query(Appointment).filter_by(slot_id=slot.id).first()
                        if appointment:
                            manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": appointment.id,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": appointment.cancel_type,
                                        "comments": appointment.comments,
                                        "course_id": appointment.course_id,
                                        "group_id": appointment.group_id,
                                        "phone": appointment.phone,
                                        "slot_id": slot.id,
                                        "zoho_link": appointment.zoho_link
                                    }
                                )
                        else:
                            manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": None,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": None,
                                        "comments": None,
                                        "course_id": None,
                                        "group_id": None,
                                        "phone": None,
                                        "slot_id": slot.id,
                                        "zoho_link": None
                                    }
                                )
                    result.append(manager_result)
            else:
                managers_ids = [int(i) for i in managers_list.split(', ')]
                for manager_id in managers_ids:
                    if not session.query(Manager).filter_by(id=manager_id).first():
                        return jsonify(message=f'Manager with id {manager_id} does not exist.'), 404
                    manager_result = {
                    "manager_appointments": []
                    }
                    manager_result["manager_id"] = manager_id
                    manager_result["manager_name"] = session.query(Manager).filter_by(id=manager_id).first().name
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=time).first()
                    if not slot:
                        manager_result["manager_appointments"].append(
                                {
                                    "time": time,
                                    "slot_id": 0,
                                    "status_id": 0
                                }
                        )
                    else:
                        appointment = session.query(Appointment).filter_by(slot_id=slot.id).first()
                        if appointment:
                            manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": appointment.id,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": appointment.cancel_type,
                                        "comments": appointment.comments,
                                        "course_id": appointment.course_id,
                                        "group_id": appointment.group_id,
                                        "phone": appointment.phone,
                                        "slot_id": slot.id,
                                        "zoho_link": appointment.zoho_link
                                    }
                                )
                        else:
                            manager_result["manager_appointments"].append(
                                    {
                                        "appointment_id": None,
                                        "status": slot.status_id,
                                        "time": slot.time,
                                        "cancel_type": None,
                                        "comments": None,
                                        "course_id": None,
                                        "group_id": None,
                                        "phone": None,
                                        "slot_id": slot.id,
                                        "zoho_link": None
                                    }
                                )
                    result.append(manager_result)
        return jsonify(data=result), 200

    except Exception as e:
        session.rollback()
        return jsonify(error=str(e)), 400