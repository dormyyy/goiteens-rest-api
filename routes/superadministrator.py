from datetime import timedelta, datetime
import backup
from app import app, session
from flask import jsonify, request
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour, to_datetime
import re

weekdays = {
    "0": "Пн",
    "1": "Вт",
    "2": "Ср",
    "3": "Чт",
    "4": "Пт",
    "5": "Сб",
    "6": "Нд"
}


@app.route('/superadmin_managers/<string:date>/<int:half>', methods=['GET'])
def superadmin_managers(date: str, half: int):
    data = {
        'date': date,
        'half': half,
        'available_managers': []
    }
    date = to_datetime(date)
    if half == 1:
        for hour in range(8, 15):
            managers = session.query(Manager).filter(Slots.manager_id == Manager.id, Slots.date == date, Slots.time == hour, Slots.status_id == 1).all()
            data['available_managers'].append({
                'time': hour,
                'managers': [manager.name for manager in managers] if managers else 'not found'
            })

    else:
        for hour in range(15, 23):
            managers = session.query(Manager).filter(Slots.manager_id == Manager.id, Slots.date == date, Slots.time == hour, Slots.status_id == 1).all()
            data['available_managers'].append({
                'time': hour,
                'managers': [manager.name for manager in managers] if managers else 'not found'
            })
    backup.backup()
    return jsonify(data=data), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    crm_link = request.form['crm_link']
    appointment = session.query(Appointment).filter_by(zoho_link=crm_link).first()
    if appointment:
        slot = session.query(Slots).filter_by(id=appointment.slot_id).first()
        if slot:
            weeks = session.query(Weeks).all()
            for i in [i.date_start for i in weeks]:
                if 0 <= (slot.date - i).days <= 7:
                    week_id = session.query(Weeks).filter_by(date_start=i).first().id
            data = {
                'appointment_id': appointment.id,
                'week_id': week_id,
                'day': slot.week_day,
                'date': slot.date,
                'weekday': weekdays.get(str(slot.week_day)),
                'hour': slot.time,
                'slot_id': appointment.slot_id,
                'course_id': appointment.course_id,
                'course': 'not found',
                'crm_link': appointment.zoho_link,
                'phone': appointment.phone,
                'age': appointment.age,
                'manager_id': slot.manager_id,
                'manager_name': 'not found'
            }
            course = session.query(Course).filter_by(id=appointment.course_id).first()
            if course:
                data['course'] = course.name
            manager = session.query(Manager).filter_by(id=slot.manager_id).first()
            if manager:
                data['manager_name'] = manager.name
        else:
            return jsonify(message='Slot not found'), 404
        try:
            backup.backup()
        except:
            pass
        return jsonify(data=data), 200
    else:
        return jsonify(message='Appointment not found'), 404


@app.route('/update_superad_appointment', methods=['POST'])
def update_superad_appointment():
    appointment_id = request.form['appointment_id']
    hour = request.form['hour']
    course_id = request.form['course_id']
    crm_link = request.form['crm_link']
    phone = request.form['phone']
    age = request.form['age']
    message = request.form['message']
    manager_id = request.form['manager_id']
    try:
        date = to_datetime(request.form['date'])
    except:
        return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 400
    
    course_managers = [i.manager_id for i in session.query(ManagerCourses).filter_by(course_id=course_id).all()]
    if int(manager_id) not in course_managers:
        return jsonify(message=f'Selected manager is not responsible for the course {course_id}'), 400

    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        appointment_slot = session.query(Slots).filter_by(id=appointment.slot_id).first()
        expected_slot = session.query(Slots).filter_by(date=date, time=hour, manager_id=manager_id).first()
        if not expected_slot:
            return jsonify(message='There are no available slots.'), 400
        appointment_slot.status_id = 1
        appointment.course_id = course_id
        appointment.zoho_link = crm_link.strip()
        appointment.phone = phone
        appointment.age = age
        appointment.message = message
        expected_slot.status_id = 3
        expected_slot.manager_id = manager_id
        appointment.slot_id = expected_slot.id
        session.commit()
        slot = expected_slot
        data = {
            'appointment_id': appointment.id,
            'day': slot.week_day,
            'date': slot.date,
            'weekday': weekdays.get(str(slot.week_day)),
            'hour': slot.time,
            'slot_id': appointment.slot_id,
            'course_id': appointment.course_id,
            'course': 'not found',
            'crm_link': appointment.zoho_link,
            'phone': appointment.phone,
            'age': appointment.age,
            'manager_id': slot.manager_id,
            'manager_name': 'not found'
        }
        course = session.query(Course).filter_by(id=appointment.course_id).first()
        if course:
            data['course'] = course.name
        manager = session.query(Manager).filter_by(id=slot.manager_id).first()
        if manager:
            data['manager_name'] = manager.name
        try:
            backup.backup()
        except:
            pass
        return jsonify(data=data), 200
    else:
        return jsonify(message='Appointment not found'), 404
    


@app.route('/manager/courses/<int:manager_id>', methods=['GET', 'POST'])
def manager_courses(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if not manager:
        return jsonify(message=f'Manager with id {manager_id} does not exist.'), 404
    manager_courses = session.query(ManagerCourses).filter_by(manager_id=manager_id)
    if request.method == 'POST':
        courses = request.form.get('courses', None)
        if not courses:
            return jsonify(message="'courses' is required field."), 400
        elif not re.match(r'^\d+(?:\s+\d+)*$', courses):
            return jsonify(message='Courses ids must be splitted by spaces.', example='1 2 3 4 5'), 400
        elif len(courses.split()) > session.query(Course).count():
            return jsonify(message=f'Too many ids entered. Available courses - {session.query(Course).count()}'), 400
        elif not all(course in [str(i.id) for i in session.query(Course)] for course in courses.split()):
            available_courses = courses_schema.dump(session.query(Course).all())
            return jsonify(message='Some of ids do not match available courses.', courses=available_courses), 400
        
        if session.query(ManagerCourses).filter_by(manager_id=manager_id).count() == 0:
            for course in set(courses.split()):
                obj = ManagerCourses(manager_id=manager_id, course_id=course)
                session.add(obj)
                session.commit()
        else:
            manager_courses.delete(synchronize_session=False)
            session.commit()
            for course in set(courses.split()):
                obj = ManagerCourses(manager_id=manager_id, course_id=course)
                session.add(obj)
                session.commit()

        courses_list = [{"id": course.id, "name": course.name} for course in session.query(Course).filter(Course.id.in_(courses.split()))]
        result = {
            manager.name: courses_list
        }
        return jsonify(message='Courses successfully added', data=result), 200
    elif request.method == 'GET':
        courses_list = [{"id": course.id, "name": course.name, "is_active": True if course.id in [i.course_id for i in manager_courses] else False} for course in session.query(Course).filter(Course.id != 1 or Course.name != 'Не призначено')]
        result = {
            "manager": manager_schema.dump(manager),
            "courses": courses_list
        }
        return jsonify(result), 200
    

@app.route('/managers_by_course/<int:course_id>/<string:date>/<int:time>', methods=['GET'])
def get_managers_by_course(course_id: int, date: str, time: int):
    if course_id not in [i.id for i in session.query(Course).all()]:
        return jsonify(message=f'Course with id {course_id} does not exist'), 404
    
    try:
        date = to_datetime(date)
    except:
        return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404
    
    course = session.query(Course).filter_by(id=course_id).first()
    managers = session.query(ManagerCourses).filter_by(course_id=course_id).join(Manager).join(Slots).filter_by(date=date, time=time, status_id=1).all()
    result = {
        "course": course_schema.dump(course),
        "is_active": True,
        "managers": []
    }

    for manager in [i.manager_id for i in managers]:
        manager_obj = session.query(Manager).filter_by(id=manager).first()
        result["managers"].append(manager_schema.dump(manager_obj))

    return jsonify(result), 200
    

@app.route('/get-date/<int:week_id>/<int:day>', methods=['GET'])
def get_date(week_id:int, day:int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    if not week:
        return jsonify(message=f'Week with id {week_id} does not exist.'), 404
    elif day not in range(0, 7):
        return jsonify(message='Day must be between 0 and 6 included.'), 400
    date = week.date_start + timedelta(days=int(day))
    formatted_date = date.strftime("%d.%m.%Y")
    return jsonify(date=formatted_date), 200