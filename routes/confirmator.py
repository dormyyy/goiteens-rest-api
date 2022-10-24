from datetime import timedelta, datetime
from flask_cors import cross_origin
from app import app, session
from flask import jsonify
from models import *
import backup
from utils.convert_str_to_datetime import get_current_date, get_current_hour
from utils import data_to_json
from operator import itemgetter
from schemas import * 
from pprint import pprint


def appointment_hour_sort(n):
    try:
        x = int(n["hour"])
        
    except TypeError:
        x=21
    print(x)
    return x

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
        appointments.append(session.query(Appointment).filter_by(slot_id=i, cancel_type=0).first())
    day = datetime.now().weekday()
    result.update({"week_id": week_id, "day": day, "half": half, "date": datetime.now().date(), "appointments": []})
    for i in appointments:
        if i is not None:
            if half == 1:
                course = session.query(Course).filter_by(id=i.course_id).first()
                if course:
                    course_name = course.name
                else:
                    course_name = 'No course'
                if session.query(Slots).filter_by(id=i.slot_id).first().time < 14:
                    try:
                        result["appointments"].append({
                            "appointment_id": i.id,
                            "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                            "course": course_name,
                            "manager_name": session.query(Manager).filter_by(
                                id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                            "crm_link": i.zoho_link,
                            "phone": i.phone,
                            "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id,
                            "slot_id": i.slot_id
                        })
                    except:
                        print('Error')
            else:
                course = session.query(Course).filter_by(id=i.course_id).first()
                if course:
                    course_name = course.name
                else:
                    course_name = 'No course'
                if session.query(Manager).filter_by(
                            id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first():
                    manager_name = session.query(Manager).filter_by(
                            id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name
                else:
                    manager_name = 'not found'
                if session.query(Slots).filter_by(id=i.slot_id).first().time >= 14:
                    try:
                        result["appointments"].append({
                            "appointment_id": i.id,
                            "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                            "course": course_name,
                            "manager_name": manager_name,
                            "crm_link": i.zoho_link,
                            "phone": i.phone,
                            "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id,
                            "slot_id": i.slot_id
                        })
                    except:
                        print('Error')
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(message="Successfully", data=result), 200


@app.route('/get_confirmation/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_confirmations(week_id: int, day: int, half: int):
    result = {}
    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    # print(date)
    slots = session.query(Slots).filter_by(date=date, status_id=3).all()
    # print(slots)
    slots_id = [i.id for i in slots]
    # print(slots_id)
    appointments = []
    # print(Appointment)
    for i in slots_id:
        print(i)
        appointments.append(session.query(Appointment).filter_by(slot_id=i, cancel_type=0).first())
    print(appointments)
    result.update({"week_id": week_id, "day": day, "half": half, "date": datetime.now().date(), "appointments": []})
    for i in appointments:
        if i is not None:
            if half == 1:
                course = session.query(Course).filter_by(id=i.course_id).first()
                if course:
                    course_name = course.name
                else:
                    course_name = 'No course'
                if session.query(Manager).filter_by(
                            id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first():
                    manager_name = session.query(Manager).filter_by(
                            id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name
                else:
                    manager_name = 'not found'
                if session.query(Slots).filter_by(id=i.slot_id).first().time < 14:
                    result["appointments"].append({
                        "appointment_id": i.id,
                        "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                        "course": course_name,
                        "manager_name": manager_name,
                        "crm_link": i.zoho_link,
                        "phone": i.phone,
                        "slot_id": i.slot_id,
                        "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id

                    })
            else:
                course = session.query(Course).filter_by(id=i.course_id).first()
                if course:
                    course_name = course.name
                else:
                    course_name = 'No course'
                if session.query(Slots).filter_by(id=i.slot_id).first().time >= 14:
                    try:
                        m_name = session.query(Manager).filter_by(
                            id=session.query(Slots).filter_by(id=i.slot_id).first().manager_id).first().name,
                    except:
                        m_name = 'Manager'
                    result["appointments"].append({
                        "appointment_id": i.id,
                        "hour": session.query(Slots).filter_by(id=i.slot_id).first().time,
                        "course": course_name,
                        "manager_name": m_name,
                        "crm_link": i.zoho_link,
                        "phone": i.phone,
                        "slot_id": i.slot_id,
                        "status": session.query(Slots).filter_by(id=i.slot_id).first().status_id
                    })
    try:
        backup.backup()
    except:
        print('', end='')
    # result = sorted(result,key = appointment_hour_sort)
    result["appointments"] = sorted(result["appointments"],key =lambda n: n['hour'] )
    # for i in result["appointments"]:
    #   print(i['hour'])
    # res = appointment_hour_sort(result)
    # print(res)
    # print(result)
    return jsonify(message="Successfully", data=result), 200


@cross_origin(supports_credentials=True)
@app.route('/set_confirmation/<int:slot_id>/<int:status>/<string:message>/', methods=['PUT', 'POST'])
def set_confirmation(slot_id: int, status: int, message: str):
    appointment = session.query(Appointment).filter_by(slot_id=slot_id).first()
    if appointment:
        appointment.comments = message
        slot = session.query(Slots).filter_by(id=slot_id).first()
        slot.status_id = status
        session.commit()
        backup.backup()
        return jsonify(message="Successfully"), 200
    else:
        return jsonify(message="Appointment not found"), 404


@cross_origin(supports_credentials=True)
@app.route('/set_cancel_confirmation/<int:slot_id>/<int:cancel_type>/<string:message>/', methods=['PUT', 'POST'])
def set_cancel_confirmations(slot_id: int, cancel_type: int, message: str):
    appointment = session.query(Appointment).filter_by(slot_id=slot_id).first()
    if appointment:
        appointment.cancel_type = cancel_type
        appointment.comments = message
        session.commit()
        backup.backup()
        return jsonify(message="Відмінено"), 200
    else:
        return jsonify(message="Appointment not found"), 404


# отримати в appointment - значення slot_id (old)
# в slot_id (new) - змінюємо значення status_id на 3 (зайнято)
# slot_id (old) - змінюємо status_id на 1 (вільно)


@cross_origin(supports_credentials=True)
@app.route('/set_postpone_confirmation/<int:slot_id>/<int:appointment_id>/', methods=['PUT', 'POST'])
def set_postpone_confirmations(slot_id: int, appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    # check
    # slot_id
    ap = appointment_schema.dump(appointment)
    print(ap)
    print(ap['slot_id'])
    slot_id_in = int(ap['slot_id'])

    # slot
    slot_jsn_in = session.query(Slots).filter_by(id=slot_id_in).first()

    print("slot_id_in: "+str(slot_jsn_in.id))
    print(slot_jsn_in.name)
    print(slot_jsn_in.date)
    print(slot_jsn_in.time)
    print(slot_jsn_in.manager_id) # Це який менеджері - від якого йдуть, а бо якого йдуть?


    slot_jsn_out = session.query(Slots).filter_by(id=slot_id).first()

    print("slot_id_out: "+str(slot_jsn_out.id))
    print(slot_jsn_out.name)
    print(slot_jsn_out.date)
    print(slot_jsn_out.time)
    print(slot_jsn_out.manager_id) # Це який менеджері - від якого йдуть, а бо якого йдуть?


    # Тут треба звернутися до менеджера
    # Менеджеру треба змінити статус.
    print(slot_jsn_in.status_id)
    print(slot_jsn_in.week_day)
    # print(sl)

    # Шукаємо менеджера для slot_id: int, який прилітає згори.

    if appointment:
        # old_slot_id = appointment.slot_id
        appointment.slot_id = slot_id
        session.commit()
        backup.backup()
        return jsonify(message="Перенесено"), 200
    else:
        return jsonify(message="Appointment not found"), 404

@app.route('/check_slots')
def check_slots():
    slot_id = 352
    slot = session.query(Slots).filter_by(id=slot_id).first()
    slot.time = slot.time + 1
    # session.commit()
    session.commit()
    print(slot.time)
    print(slot)
    print(slot.id)    
    # print(slots_schema.dump(slot))
    return str(slot.time)