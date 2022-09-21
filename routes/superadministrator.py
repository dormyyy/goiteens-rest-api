from datetime import timedelta, datetime
import backup
from app import app, session
from flask import jsonify, request
from models import *
from schemas import *
from utils.convert_str_to_datetime import get_current_date, get_current_hour, to_datetime

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
        backup.backup()
        return jsonify(data=data), 200
    else:
        return jsonify(message='Appointment not found'), 404


@app.route('/update_superad_appointment', methods=['POST'])
def update_superad_appointment():
    appointment_id = request.form['appointment_id']
    week_id = request.form['week_id']
    day = request.form['day']
    hour = request.form['hour']
    course_id = request.form['course_id']
    crm_link = request.form['crm_link']
    phone = request.form['phone']
    age = request.form['age']
    manager_id = request.form['manager_id']
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        appointment_slot = session.query(Slots).filter_by(id=appointment.slot_id).first()
        date = session.query(Weeks).filter_by(id=week_id).first().date_start + timedelta(days=int(day))
        expected_slot = session.query(Slots).filter_by(date=date, time=hour, manager_id=1).first()
        if not expected_slot:
            expected_slot = session.query(Slots).filter_by(date=date, time=hour, manager_id=manager_id).first()
        if expected_slot:
            appointment_slot.status_id = 1
            appointment.course_id = course_id
            appointment.zoho_link = crm_link
            appointment.phone = phone
            appointment.age = age
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
        else:
            return jsonify(message='Slot not found'), 404
        backup.backup()
        return jsonify(data=data), 200
    else:
        return jsonify(message='Appointment not found'), 404