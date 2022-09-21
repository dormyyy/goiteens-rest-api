from datetime import timedelta
import backup
import json
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour
from utils import data_to_json


@app.route('/current_work_week/<int:manager_id>', methods=['GET'])
def get_current_work_week(manager_id: int):
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if 0 <= (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        current_week = session.query(Weeks).filter_by(id=current_week_id).first()
        template = [{"time": i, "color": 0, "slot_id": 0} for i in range(8, 23)]
        current_week_days = []
        result = []
        for i in range(0, 7):
            current_week_days.append(current_week.date_start + timedelta(days=i))
        for date in current_week_days:
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
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(current_week_id=current_week_id, current_week_date_start=current_week.date_start,
                       manager_id=manager_id, slots=result), 200
    else:
        return jsonify(message='This manager does not exist'), 409


@app.route('/get_work_week/<int:manager_id>/<int:week_id>', methods=['GET'])
def get_work_week(manager_id: int, week_id:int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    week = session.query(Weeks).filter_by(id=week_id).first()
    if manager and week:
        template = [{"time": i, "color": 0, "slot_id": 0} for i in range(8,23)]
        current_week_days = []
        result = []
        for i in range(0,7):
            current_week_days.append(week.date_start + timedelta(days=i))
        for date in current_week_days:
            current_day_slots = []
            slots = session.query(Slots).filter_by(manager_id=manager_id, date=date).all()
            if len(slots) == 0:
                result.extend([template])
            else:
                for i in range(8,23):
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).all()
                    if i in [j for j in current_day_slots]:
                        continue
                    if len(slot) == 0:
                        current_day_slots.append({"time": i, "color": 0, "slot_id": 0})
                    else:
                        current_day_slots.append({"time": i, "color": slot[0].status_id, "slot_id": slot[0].id})
            result.extend([current_day_slots])
        for i in result:
            if i == []:
                result.remove(i)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(current_week_id=week_id, current_week_date_start=week.date_start,
        manager_id=manager_id, slots=result), 200
    else:
        return jsonify(message='Manager or week do not exist'), 409


@app.route('/start_consultation/<int:week_id>/<int:week_day>/<int:time>/<int:manager_id>/', methods=['POST', 'PUT'])
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
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(message='Консультація розпочалася', data=result), 200
        else:
            return jsonify(message="Invalid time field"), 409
    else:
        return jsonify(message="Manager or week does not exist"), 404


@app.route('/consultation_result/<int:slot_id>/<int:consultation_result>/<int:group_id>/<string:message>', methods=['POST'])
def set_consultation_result(slot_id: int, consultation_result: int, group_id: int, message: str):
    slot = session.query(Slots).filter_by(id=slot_id).first()
    if slot:
        appointment = session.query(Appointment).filter_by(slot_id=slot.id).first()
        if not appointment:
            if consultation_result in [i.id for i in session.query(Status).all()]:
                slot.status_id = consultation_result
                if group_id in [i.id for i in session.query(Group).all()]:
                    appointment_group_id = group_id
                else:
                    return jsonify(message=f'Group with id {group_id} does not exist'), 404
                course_id = session.query(Group).filter_by(id=group_id).first().course_id
                appointment_phone = 0
                appointment = Appointment(zoho_link='', slot_id=slot_id,
                course_id=course_id, group_id=appointment_group_id, comments=message, phone=appointment_phone)
                session.add(appointment)  
                session.commit()
                return jsonify(message='Status successfully changed'), 200
            else:
                return jsonify(message=f'Status code {consultation_result} does not exist'), 404
        else:
            if consultation_result in [i.id for i in session.query(Status).all()]:
                slot.status_id = consultation_result
                appointment.group_id = group_id
                appointment.comments = message
                session.commit()
                backup.backup()
                return jsonify(message='Status successfully changed'), 200
            else:
                return jsonify(message='Status does not exist'), 404
    else:
        return jsonify(message='Slot does not exist'), 404

