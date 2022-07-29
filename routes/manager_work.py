from datetime import timedelta
import ast
import json
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour


@app.route('/current_work_week/<int:manager_id>', methods=['GET'])
def get_current_work_week(manager_id: int):
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if 0 < (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        current_week = session.query(Weeks).filter_by(id=current_week_id).first()
        template = [{"time": i, "color": 0, "slot_id": 0} for i in range(8, 23)]
        currnet_week_days = []
        result = []
        for i in range(0, 7):
            currnet_week_days.append(current_week.date_start + timedelta(days=i))
        for date in currnet_week_days:
            current_day_slots = []
            slots = session.query(Slots).filter_by(manager_id=manager_id, date=date).all()
            if len(slots) == 0:
                result.extend([template])
            else:
                for i in range(8, 23):
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).all()
                    if i in [j for j in current_day_slots]:
                        continue
                    if len(slot) == 0:
                        current_day_slots.append({"time": i, "color": 0, "slot_id": 0})
                    else:
                        current_day_slots.append({"time": i, "color": slot[0].status_id, "slot_id": slot[0].id})
            result.extend([current_day_slots])
        for i in result:
            if not i:
                result.remove(i)
        return jsonify(current_week_id=current_week_id, current_week_date_start=current_week.date_start,
                       manager_id=manager_id, slots=result), 200
    else:
        return jsonify(message='This manager does not exist'), 409


@app.route('/start_consultation/<int:week_id>/<int:week_day>/<int:time>/<int:manager_id>/', methods=['POST'])
def start_consultation(week_id: int, week_day: int, time: int, manager_id: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager and week:
        if time in range(8, 23):
            slot_date = week.date_start + timedelta(days=week_day)
            slot = session.query(Slots).filter_by(date=slot_date, time=time, manager_id=manager_id).first()
            slot.status_id = 6
            session.commit()
            result = slot_schema.dump(slot)
            return jsonify(message='Консультація розпочалася', data=result), 200
        else:
            return jsonify(message="Invalid time field"), 409
    else:
        return jsonify(message="Manager or week does not exist"), 404
