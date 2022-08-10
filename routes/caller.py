from datetime import timedelta, datetime
import ast
from email import message
import json
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour


@app.route('/caller_current_week', methods=['GET'])
def get_caller_current_week():
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if 0 <= (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
    current_week = session.query(Weeks).filter_by(id=current_week_id).first()
    template = [{"time": i, "amount": 0} for i in range(8,23)]
    currnet_week_days = []
    result = []
    for i in range(0,7):
        currnet_week_days.append(current_week.date_start + timedelta(days=i))
    for date in currnet_week_days:
        current_day_slots = []
        slots = session.query(Slots).filter_by(date=date, status_id=1).all()
        if len(slots) == 0:
            result.extend([template])
        else:
            for i in range(8, 23):
                slot = session.query(Slots).filter_by(date=date, time=i, status_id=1).all()
                if i in [j for j in current_day_slots]:
                    continue
                if len(slot) == 0:
                    current_day_slots.append({"time": i, "amount": 0})
                else:
                    current_day_slots.append({"time": i, "amount": len(slot)})
        result.extend([current_day_slots])
    for i in result:
        if i == []:
            result.remove(i)
    return jsonify(current_week_id=current_week_id, current_week_date_start=current_week.date_start, slots=result), 200


@app.route('/get_caller_week/<int:week_id>', methods=['GET'])
def get_caller_week(week_id: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    if not week:
        return jsonify(message='Week does not exist'), 404
    else:
        template = [{"time": i, "amount": 0} for i in range(8,23)]
        currnet_week_days = []
        result = []
        for i in range(0,7):
            currnet_week_days.append(week.date_start + timedelta(days=i))
        for date in currnet_week_days:
            current_day_slots = []
            slots = session.query(Slots).filter_by(date=date, status_id=1).all()
            if len(slots) == 0:
                result.extend([template])
            else:
                for i in range(8, 23):
                    slot = session.query(Slots).filter_by(date=date, time=i, status_id=1).all()
                    if i in [j for j in current_day_slots]:
                        continue
                    if len(slot) == 0:
                        current_day_slots.append({"time": i, "amount": 0})
                    else:
                        current_day_slots.append({"time": i, "amount": len(slot)})
            result.extend([current_day_slots])
        for i in result:
            if i == []:
                result.remove(i)
        return jsonify(current_week_id=week.id, current_week_date_start=week.date_start, slots=result), 200


@app.route('/avaliable_managers/<int:week_id>/<int:week_day>/<int:hour>', methods=['GET'])
def get_avaliable_managers(week_id: int, week_day: int, hour: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    slot_date = week.date_start + timedelta(days=week_day)
    managers = session.query(Manager).filter(Slots.manager_id == Manager.id, Slots.date == slot_date, Slots.time == hour, Slots.status_id == 1).all()
    for i in range(len(managers)-1):
        for j in range(0, len(managers)-i-1):
            manager_slots1 = session.query(Slots).filter_by(manager_id=managers[j].id, date=slot_date, status_id=1).all()
            manager_slots2 = session.query(Slots).filter_by(manager_id=managers[j+1].id, date=slot_date, status_id=1).all()
            if len(manager_slots1) > len(manager_slots2):
                managers[j], managers[j+1] = managers[j+1], managers[j]
    result = [{'manager_id': i.id, 'name': i.name} for i in managers]
    return jsonify(data=result), 200


@app.route('/create_appointment/<int:week_id>/<int:day>/<int:hour>/<int:course_id>/<string:crm_link>/<string:phone>/<int:age>/<int:manager_id>', methods=['POST', 'PUT'])
def create_appointment(week_id: int, day: int, hour: int, course_id: int, crm_link: str, phone: str, age: int, manager_id: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    slot_date = week.date_start + timedelta(days=day)
    slot = session.query(Slots).filter_by(date=slot_date, time=hour).first()
    slot_status = 3
    if slot:
        slot.manager_id = manager_id
        slot.status_id = slot_status
        appointment = Appointment(slot_id=slot.id, course_id=course_id, phone=phone, age=age, zoho_link=crm_link, group_id=1)
        session.add(appointment)
        session.commit()
        data = {
            "week_id": week_id,
            "day_id": day,
            "hour": hour,
            "slot_id": slot.id,
            "course_id": course_id,
            "crm_link": crm_link,
            "phone": phone,
            "age": age,
            "manager_id": manager_id
        }
        return jsonify(message='Appointment successfully created', data=data), 200
    else:
        return jsonify(message='Slot not found'), 404
