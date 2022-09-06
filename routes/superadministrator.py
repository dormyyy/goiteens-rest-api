from datetime import timedelta, datetime
from email import message
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
    return jsonify(data=data), 200


@app.route('/search', methods=['GET'])
def search():
    crm_link = request.form['crm_link']
    appointment = session.query(Appointment).filter_by(zoho_link=crm_link).first()
    if appointment:
        slot = session.query(Slots).filter_by(id=appointment.slot_id).first()
        if slot:
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
        return jsonify(data=data), 200
    else:
        return jsonify(message='Appointment not found'), 404
