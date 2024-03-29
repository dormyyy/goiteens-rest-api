from datetime import timedelta, datetime
from multiprocessing.dummy import Manager
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


@app.route('/current_confirmed', methods=['GET'])
def get_current_confirmeds():
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
    slots = session.query(Slots).filter_by(date=date, status_id=4).all()
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

@app.route('/get_confirmation_manager/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_confirmations_manager(week_id: int, day: int, half: int):
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
                        "course": ["One","two","three"], #course_name
                        "manager_name": "name", #m_name
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
                        "course": ["One","two","three"], #course_name
                        "manager_name": "name", #m_name
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


# Сделать функцию для получения структуры слота.
@app.route('/get_avaliable_manager/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_avaliable_manager(week_id: int, day: int, half: int):
    result = {}
    rng = range(8,14) if half ==1 else range(14,23)

    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    appointments = []
    for time in rng:
        slots = session.query(Slots).filter_by(date=date, status_id=1 ,time = time).all()
        slots_id = []
        managers_names = []
        appointment = []
        if slots:
            for i in slots:
                manager_name = session.query(Manager).filter_by(
                                id=session.query(Slots).filter_by(id=i.id).first().manager_id).first().name
                manager_id = session.query(Manager).filter_by(
                                id=session.query(Slots).filter_by(id=i.id).first().manager_id)
                appointment.append({"hour":time,"appointment_id":i.manager_id,"manager_name":manager_name})
        else:
            appointment.append({"hour":time,"appointment_id":0,"manager_name":"none"})

        appointments.append(appointment)
    result.update({"week_id": week_id, "day": day, "half": half, "date": datetime.now().date(), "appointments": appointments})

    try:
        backup.backup()
    except:
        print('', end='')
    # result = sorted(result,key = appointment_hour_sort)
    # result["appointments"] = sorted(result["appointments"],key =lambda n: n['hour'] )
    return jsonify(message="Successfully", data=result), 200


@app.route('/get_current_avaliable_manager/', methods=['GET'])
def get_current_avaliable_manager():
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
    day = datetime.now().weekday()
    print(week_id,day,half)

    rng = range(8,14) if half ==1 else range(14,23)

    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    appointments = []
    for time in rng:
        slots = session.query(Slots).filter_by(date=date, status_id=1 ,time = time).all()
        slots_id = []
        managers_names = []
        appointment = []
        if slots:
            for i in slots:
                manager_name = session.query(Manager).filter_by(
                                id=session.query(Slots).filter_by(id=i.id).first().manager_id).first().name
                manager_id = session.query(Manager).filter_by(
                                id=session.query(Slots).filter_by(id=i.id).first().manager_id)
                appointment.append({"hour":time,"appointment_id":i.manager_id,"manager_name":manager_name})
        else:
            appointment.append({"hour":time,"appointment_id":0,"manager_name":"none"})

        appointments.append(appointment)
    result.update({"week_id": week_id, "day": day, "half": half, "date": datetime.now().date(), "appointments": appointments})

    try:
        backup.backup()
    except:
        print('', end='')
    # result = sorted(result,key = appointment_hour_sort)
    # result["appointments"] = sorted(result["appointments"],key =lambda n: n['hour'] )
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


@app.route('/get_confirmed/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_confirmed(week_id: int, day: int, half: int):
    result = {}
    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    # print(date)
    # status = 4 - підтверджено
    slots = session.query(Slots).filter_by(date=date, status_id=4).all()
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
    slot = session.query(Slots).filter_by(id=slot_id).first()
    # Отримуємо slot_id
    # У slot_id - змінюємо статус

    # Змінити статус слота на 1.
    if appointment:
        appointment.cancel_type=cancel_type
        appointment.comments=message
        appointment.slot_id=None
        appointment.zoho_link=None
        slot.status_id=1
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
    # Отримаємо той slot_id, який є у поточного appoitment
    print(ap)
    print(ap['slot_id'])
    slot_id_in = int(ap['slot_id'])

    # Рогортаємо slot_id - який є у поточного appoitment (той, з якого уходять - out)
    slot_jsn_in = session.query(Slots).filter_by(id=slot_id_in).first()

    print("slot_id_in: "+str(slot_jsn_in.id))
    print(slot_jsn_in.name)
    print(slot_jsn_in.date)
    print(slot_jsn_in.time)
    print(slot_jsn_in.manager_id) # Це який менеджері - від якого йдуть (out)

    slot_jsn_in.status_id = 1

    manager_in_obj =  session.query(Manager).filter_by(id=slot_jsn_in.manager_id).first()

    print("manager_in " + str(manager_in_obj.name))

    # От тут - змінюємо в цього менеджеру status_id на 1.


    # Робимо запит до таблиці - за id, який приходить
    slot_jsn_out = session.query(Slots).filter_by(id=slot_id).first()

    print("slot_id_out: "+str(slot_jsn_out.id))
    print(slot_jsn_out.name)
    print(slot_jsn_out.date)
    print(slot_jsn_out.time)
    print(slot_jsn_out.manager_id) # Це який менеджері - до якого йдуть

    slot_jsn_out.status_id = 3

    # Робимо запит до бд за менеджера
    manager_out_obj =  session.query(Manager).filter_by(id=slot_jsn_out.manager_id).first()

    print("manager_out" + str(manager_out_obj.name))

    # Тут треба звернутися до менеджера і поставити йому status_id = 3

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