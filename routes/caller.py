from datetime import timedelta, datetime
from app import app, session
from flask import jsonify
from models import *
from utils.convert_str_to_datetime import get_current_date


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


@app.route('/avaliable_managers/<int:week_id>/<int:week_day>/<int:hour>', methods=['GET'])
def get_avaliable_managers(week_id: int, week_day: int, hour: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    slot_date = week.date_start + timedelta(days=week_day)
    managers = session.query(Manager).filter(Slots.manager_id == Manager.id, Slots.date == slot_date, Slots.status_id == 1).all()
    for i in range(len(managers)-1):
        for j in range(0, len(managers)-i-1):
            manager_slots1 = session.query(Slots).filter_by(manager_id=managers[j].id, date=slot_date, status_id=1).all()
            manager_slots2 = session.query(Slots).filter_by(manager_id=managers[j+1].id, date=slot_date, status_id=1).all()
            if len(manager_slots1) > len(manager_slots2):
                managers[j], managers[j+1] = managers[j+1], managers[j]
    result = [{'manager_id': i.id, 'name': i.name} for i in managers]
    return jsonify(data=result), 200