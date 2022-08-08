from datetime import timedelta, datetime
from flask_cors import cross_origin
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour


@app.route('/current_confirmation', methods=['GET'])
def get_current_confirmations():
    result = {}
    date = get_current_date()
    weeks = session.query(Weeks).all()
    if get_current_hour() >= 14:
        half = 2
    else:
        half = 1
    for i in [i.date_start for i in weeks]:
        if 0 <= (date - i).days <= 7:
            week_id = session.query(Weeks).filter_by(date_start=i).first().id
    slots = session.query(Slots).filter_by(date=date, status_id=3).all()
    slots_id = [i.id for i in slots]
    appointments = []
    for i in slots_id:
        appointments.append(session.query(Appointment).filter_by(slot_id=i).first())
    day = datetime.now().weekday()
    result.update({"week_id": week_id, "day": day, "half": half, "appointments": []})
    for i in appointments:
        if half == 1:
            if session.query(Slots).filter_by(id=i.slot_id).first().time < 14:
                result["appointments"].append({
                    "appointment_id": i.id,
                    "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                    "course": session.query(Course).filter_by(id=i.course_id).first().name,
                    "manager_name": session.query(Manager).filter_by(
                        id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                    "phone": i.phone,
                    "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id,
                    "slot_id": i.slot_id
                })
        else:
            if session.query(Slots).filter_by(id=i.slot_id).first().time >= 14:
                result["appointments"].append({
                    "appointment_id": i.id,
                    "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                    "course": session.query(Course).filter_by(id=i.course_id).first().name,
                    "manager_name": session.query(Manager).filter_by(
                        id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                    "phone": i.phone,
                    "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id,
                    "slot_id": i.slot_id
                })
    return jsonify(message="Successfully", data=result), 200


@app.route('/get_confirmation/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_confirmations(week_id: int, day: int, half: int):
    result = {}
    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    slots = session.query(Slots).filter_by(date=date, status_id=3).all()
    slots_id = [i.id for i in slots]
    appointments = []
    for i in slots_id:
        appointments.append(session.query(Appointment).filter_by(slot_id=i).first())
    result.update({"week_id": week_id, "day": day, "half": half, "appointments": []})
    for i in appointments:
        if half == 1:
            if session.query(Slots).filter_by(id=i.slot_id).first().time < 14:
                result["appointments"].append({
                    "appointment_id": i.id,
                    "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                    "course": session.query(Course).filter_by(id=i.course_id).first().name,
                    "manager_name": session.query(Manager).filter_by(
                        id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                    "phone": i.phone,
                    "slot_id": i.slot_id,
                    "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id

                })
        else:
            if session.query(Slots).filter_by(id=i.slot_id).first().time >= 14:
                result["appointments"].append({
                    "appointment_id": i.id,
                    "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                    "course": session.query(Course).filter_by(id=i.course_id).first().name,
                    "manager_name": session.query(Manager).filter_by(
                        id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                    "phone": i.phone,
                    "slot_id": i.slot_id,
                    "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id
                })
    return jsonify(message="Successfully", data=result), 200


@cross_origin(supports_credentials=True)
@app.route('/set_confirmation/<int:slot_id>/<int:status>/<string:message>/', methods=['PUT'])
def set_confirmation(slot_id: int, status: int, message: str):
    appointment = session.query(Appointment).filter_by(slot_id=slot_id).first()
    if appointment:
        appointment.comments = message
        slot = session.query(Slots).filter_by(id=slot_id).first()
        slot.status_id = status
        session.commit()
        return jsonify(message="Successfully"), 200
    else:
        return jsonify(message="Appointment not found"), 404


@cross_origin(supports_credentials=True)
@app.route('/set_cancel_confirmation/<int:slot_id>/<int:cancel_type>/<string:message>/', methods=['PUT'])
def set_cancel_confirmations(slot_id: int, cancel_type: int, message: str):
    appointment = session.query(Appointment).filter_by(slot_id=slot_id).first()
    if appointment:
        appointment.cancel_type = cancel_type
        appointment.comments = message
        session.commit()
        return jsonify(message="Відмінено"), 200
    else:
        return jsonify(message="Appointment not found"), 404


@cross_origin(supports_credentials=True)
@app.route('/set_postpone_confirmation/<int:slot_id>/<int:appointment_id>/', methods=['PUT'])
def set_postpone_confirmations(slot_id: int, appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        appointment.slot_id = slot_id
        session.commit()
        return jsonify(message="Перенесено"), 200
    else:
        return jsonify(message="Appointment not found"), 404
