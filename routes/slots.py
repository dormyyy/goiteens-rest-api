from email import message

import backup
from app import app, session
from flask import request, jsonify
from models import *
from schemas import * 
from utils.convert_str_to_datetime import to_datetime
from utils import data_to_json

# Додати перевірки інших слотів на цей час/дату та менеджера.
# slots table routers {
@app.route('/register_slot', methods=['POST'])
def register_slot():
    name = request.form['name']
    slot = session.query(Slots).filter_by(name=name).first()
    managers = session.query(Manager).all()
    statuses = session.query(Status).all()
    if slot:
        return jsonify(message='This slot already exist'), 409
    else:
        slot_name = name
        try:
            slot_date = to_datetime(request.form['date'])
        except:
            return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404

        try: 
            if int(request.form['time']) in range(8,23):
                time = request.form['time']
        except:
            return jsonify(message='Invalid time field'), 404
        slot_manager_id = request.form['manager_id']
        slot_status_id = request.form['status_id']
        slot_week_day = request.form['week_day']

        try:
            if int(slot_manager_id) in [i.id for i in managers] and int(slot_status_id) in [i.id for i in statuses]:
                slot = Slots(name=slot_name, date=slot_date, time=time,
                manager_id=slot_manager_id, status_id=slot_status_id, week_day=slot_week_day)
                session.add(slot)
                session.commit()
                slot = session.query(Slots).filter_by(name=name).first()
                data = slot_schema.dump(slot)
                try:
                    data_to_json.to_json(data)
                except:
                    print('', end='')
                return jsonify(data=data, message=f'Slot {slot.id} successfully registered'), 201
            else:
                return jsonify(message=f'Invalid manager id or status_id'), 404
        except:
            return jsonify(message=f'Invalid manager id or status_id'), 404


@app.route('/remove_slot/<int:slot_id>', methods=['DELETE'])
def remove_slot(slot_id: int):
    slot = session.query(Slots).filter_by(id=slot_id).first()
    if slot:
        session.delete(slot)
        session.commit()
        return jsonify(message=f'Slot {slot.id} successfully deleted.'), 202
    else:
        return jsonify(message='Slot does not exist'), 404


@app.route('/slots', methods=['GET'])
def get_slots():
    slots_list = session.query(Slots).all()
    result = slots_schema.dump(slots_list)
    try:
        data_to_json.to_json(result)
    except:
        print('', end='')
    backup.backup()
    return jsonify(data=result)

# При зміні слоту - змінюється статус у базового менеджера і змінюється у цільового.
@app.route('/update_slot/<int:slot_id>', methods=['PUT'])
def update_slot(slot_id: int):
    # --> Дописати зміну статуса у менеджера.
    # Отримаємо слот за id для записів таблиці slot.
    slot = session.query(Slots).filter_by(id=slot_id).first()
    # Отримаємо всіх менеджерів
    managers = session.query(Manager).all()
    # Отримаємо всіх статусів
    statuses = session.query(Status).all()

    if slot:
        # Продивляємося всі ключі із формою.
        for key in request.form:
            if key == 'name':
                slot.name = request.form['name']
            elif key == 'date':
                try:
                    # конвертуємо дату до змінної
                    slot_date = to_datetime(request.form['date'])
                except:
                    return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404 
                finally:
                    # Зберігаємо дату до слоту
                    slot.date = slot_date
            elif key == 'time':
                time = request.form['time']
                try:
                    if int(time) in range(8,23):
                        slot.time = time
                except:
                    return jsonify(message='Invalid time field'), 404
            elif key == 'manager_id':
                slot_manager_id = request.form['manager_id']
                if int(slot_manager_id) in [i.id for i in managers]:
                    slot.manager_id = slot_manager_id
                else:
                    return jsonify(message='Invalid manager_id field')
            elif key == 'status_id':
                slot_status_id = request.form['status_id']
                if int(slot_status_id) in [i.id for i in statuses]:
                    slot.status_id = slot_status_id
                else:
                    return jsonify(message='Invalid status_id field')
            elif key == 'week_day':
                try:
                    week_day = request.form['week_day']
                    if week_day not in range(0,6):
                        return jsonify(message='Invalid week_day field (must be in range 0-6)'), 404
                except:
                    return jsonify(message='Invalid week_day field'), 404
                slot.week_day = week_day
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        slot = session.query(Slots).filter_by(id=slot_id).first()
        data = slot_schema.dump(slot)
        try:
            data_to_json.to_json(data)
        except:
            print('', end='')
        return jsonify(data=data, message=f'Slot {slot.id} successfully updated'), 202
    else:
        return jsonify(message='This slot does not exist'), 404
# slots table routers }

@app.route('/logs_test')
def logs():
    f = open('log.txt', 'r+', encoding='utf-8')
    log_file = f.read()
    log_file +='some test \n'
    f.close()
    f = open('log.txt', 'w', encoding='utf-8')
    f.write(log_file)
    f.close()
    return 'ok'

@app.route('/file')
def log_files():
    dt = {
    "id":1,
    "name":"Не призначено",
    "description":"1"
    }
    data_to_json.to_json_test(dt)
    return dt


# get slots on date by manager id {
@app.route('/slots_test/<int:manager_id>/<string:slot_date>')
def get_slots_by_date_test(manager_id: int, slot_date: str):
    try:
        date = to_datetime(slot_date)
    except:
        return jsonify(message='Invalid date format. Please match the format dd.mm.yyyy'), 404
    slots_list = session.query(Slots).filter_by(manager_id=manager_id, date=date)
    result = slots_schema.dump(slots_list)
    try:
        data_to_json.to_json(result)
    except:
        print('', end='')
    return jsonify(data=result)

# get slots on date by manager id }


# get slots on date by manager id {
@app.route('/slots/<int:manager_id>/<string:slot_date>')
def get_slots_by_date(manager_id: int, slot_date: str):
    try:
        date = to_datetime(slot_date)
    except:
        return jsonify(message='Invalid date format. Please match the format dd.mm.yyyy'), 404
    slots_list = session.query(Slots).filter_by(manager_id=manager_id, date=date)
    result = slots_schema.dump(slots_list)
    try:
        data_to_json.to_json(result)
    except:
        print('', end='')
    return jsonify(data=result)

# get slots on date by manager id }