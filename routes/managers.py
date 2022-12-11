import backup
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils import data_to_json

# /manager/register
@app.route('/register_manager', methods=['POST'])
def create_manager():
    name = request.form['name']
    test = session.query(Manager).filter_by(name=name).first()
    if test:
        return jsonify(message='This manager already exist'), 409
    else:
        try:
            manager_name = request.form['name']
            telegram = request.form['telegram']
            login = request.form['login']
            password = request.form['password']
            manager = Manager(name=manager_name, telegram=telegram, login=login, password=password)
            session.add(manager)
            session.commit()
            test = session.query(Manager).filter_by(name=name).first()
            data = manager_schema.dump(test)
            try:
                backup.backup()
            except:
                print('', end='')
            return jsonify(data=data, message=f'Manager {manager.id} successfully registered'), 201
        except:
            return jsonify(message='Perhaps you forgot one of required fields'), 409


# /manager/remove/<int:manager_id>
@app.route('/remove_manager/<int:manager_id>', methods=['DELETE'])
def remove_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        session.delete(manager)
        session.commit()
        backup.backup()
        return jsonify(message=f'Manager {manager.id} successfully deleted.'), 202
    else:
        return jsonify(message='Manager does not exist'), 404


@app.route('/managers', methods=['GET'])
def get_managers():
    managers_list = session.query(Manager).all()
    result = managers_schema.dump(managers_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)

@app.route('/avaliable_managers', methods=['GET'])
def get_avaliable_managers():
    managers_list = session.query(Manager).all()
    result = managers_schema.dump(managers_list)
    try:
        backup.backup()
    except:
        print('', end='')
    return jsonify(data=result)

@app.route('/av_managers/<int:week_id>/<int:day>/<int:half>/', methods=['GET'])
def get_av_managers():
    result = {}
    date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=day)
    # print(date)
    slots = session.query(Slots).filter_by(date=date, status_id=1).all()
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


# /manager/update/<int:manager_id>
@app.route('/update_manager/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        for key in request.form:
            if key == 'name':
                manager.name = request.form['name']
            elif key == 'telegram':
                manager.telegram = request.form['telegram']
            elif key == 'login':
                manager.login = request.form['login']
            elif key == 'password':
                manager.password = request.form['password']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        manager = session.query(Manager).filter_by(id=manager_id).first()
        data = manager_schema.dump(manager)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=data, message=f'Manager {manager.name} successfully updated'), 202
    else:
        return jsonify(message='This manager does not exist.'), 404


@app.route('/manager/<string:manager_name>', methods=['GET'])
def get_manager_by_name(manager_name: str):
    manager = session.query(Manager).filter_by(name=manager_name).first()
    if manager:
        result = manager_schema.dump(manager)
        try:
            backup.backup()
        except:
            print('', end='')
        return jsonify(data=result), 200
    else:
        return jsonify(message='Manager does not exists'), 404