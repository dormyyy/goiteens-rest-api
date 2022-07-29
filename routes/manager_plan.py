from datetime import timedelta
import ast
from app import app, session
from flask import jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date

@app.route('/current_week/<int:manager_id>', methods=['GET'])
def get_current_manager_week(manager_id: int):
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        print((current_date-i).days)
        if 0 < (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        current_week = session.query(Weeks).filter_by(id=current_week_id).first()
        template = [{"time": i, "color": 0, "slot_id": -1} for i in range(8,23)]
        currnet_week_days = []
        result = []
        for i in range(0,7):
            currnet_week_days.append(current_week.date_start + timedelta(days=i))
        for date in currnet_week_days:
            current_day_slots = []
            slots = session.query(Slots).filter_by(manager_id=manager_id, date=date).all()
            if len(slots) == 0:
                result.extend([template])
            else:
                for i in range(8,23):
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).all()
                    if i in [j for j in current_day_slots]:
                        print([j for j in current_day_slots])
                        continue
                    if len(slot) == 0:
                        current_day_slots.append({"time": i, "color": 0, "slot_id": -1})
                    else:
                        current_day_slots.append({"time": i, "color": slot[0].status_id, "slot_id": slot[0].id})
            result.extend([current_day_slots])
        for i in result:
            if i == []:
                result.remove(i) 
        return jsonify(current_week_id=current_week_id, current_week_date_start=current_week.date_start,
        manager_id=manager_id, slots=result), 200
    else:
        return jsonify(message='This manager does not exist'), 409


@app.route('/get_week/<int:manager_id>/<int:week_id>', methods=['GET'])
def get_week(manager_id: int, week_id:int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    week = session.query(Weeks).filter_by(id=week_id).first()
    if manager and week:
        template = [{"time": i, "color": 0} for i in range(8,23)]
        currnet_week_days = []
        result = []
        for i in range(0,7):
            currnet_week_days.append(week.date_start + timedelta(days=i))
        for date in currnet_week_days:
            current_day_slots = []
            slots = session.query(Slots).filter_by(manager_id=manager_id, date=date).all()
            if len(slots) == 0:
                result.extend([template])
            else:
                for i in range(8,23):
                    slot = session.query(Slots).filter_by(manager_id=manager_id, date=date, time=i).all()
                    if i in [j for j in current_day_slots]:
                        print([j for j in current_day_slots])
                        continue
                    if len(slot) == 0:
                        current_day_slots.append({"time": i, "color": 0})
                    else:
                        current_day_slots.append({"time": i, "color": slot[0].status_id})
            result.extend([current_day_slots])
        for i in result:
            if i == []:
                result.remove(i) 
        print(result)
        return jsonify(current_week_id=week_id, current_week_date_start=week.date_start,
        manager_id=manager_id, slots=result), 200
    else:
        return jsonify(message='Manager or week do not exist'), 409


@app.route('/update_slot/<int:manager_id>/<int:week_id>/<int:week_day>/<int:hour>/<int:new_status>', methods=['POST'])
def update_slot_status(manager_id:int, week_id: int, week_day:int, hour: int, new_status: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    week_days = []
    for i in range(0,7):
        week_days.append(week.date_start + timedelta(days=i))
    for i in week_days:
        slot = session.query(Slots).filter_by(week_day=week_day, date=i, time=hour, manager_id=manager_id).first()
        if slot != None:
            break
    else: 
        date = week.date_start + timedelta(days=week_day)
        slot = Slots(week_day=week_day, time=hour, date=date, status_id=1, manager_id=manager_id)
        session.add(slot)
        session.commit()
        return jsonify(message='Slot successfuly registered'), 200
    
    statuses = [0] + [i.id for i in session.query(Status).all()]
    if new_status not in statuses:
        return jsonify(message='This status does not exist')
    else:
        slot.status_id = new_status
        session.commit()
        return jsonify(message=f'Slot {slot.id} status successfully updated on {new_status}'), 200


@app.route('/get_template/<int:manager_id>', methods=['GET'])
def get_template(manager_id: int):
    template = session.query(Templates).filter_by(manager_id=manager_id).first()
    if template:
        result = template_schema.dump(template)
        return jsonify(data=result), 200
    else:
        return jsonify(template_id=0, message='No saved templates'), 404


@app.route('/save_template/<int:manager_id>/<string:template>', methods=['POST'])
def save_template(manager_id: int, template: str):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        list = ast.literal_eval(template)
        if len(list) == 7:
            for i in list:
                if len(i) != 15:
                    return jsonify(message="Wrong template's template"), 409
        else:
            return jsonify("Wrong template's template"), 409 
        
        new_template = Templates(manager_id=manager_id, template=template)
        session.add(new_template)
        session.commit()
        return jsonify(message='Template successfully saved.'), 200