from app import app, session
from flask import request, jsonify
from models import *
from schemas import *


@app.route('/analytics/scheduled_nc/<int:month>', methods=['GET'])
def get_not_confirmed_slots(month: int):
    managers = session.query(Manager).all()
    total_amount = len(session.query(Slots).filter(
        Slots.status_id == 3, func.extract('month', Slots.date) == month).all())
    result = {
        'amount': total_amount,
        'managers': []
    }

    for manager in managers:
        number_of_slots = len(session.query(Slots).filter(Slots.status_id == 3, func.extract('month', Slots.date) == month, Slots.manager_id == manager.id).all())
        result['managers'].append(
            {
                'manager': manager.name,
                'number_of_slots': number_of_slots,
                'absolute_value': (number_of_slots * 100 / total_amount) if total_amount > 0 else 0
            }
        )

    result['managers'].sort(key=lambda x: x['number_of_slots'], reverse=True)
    return jsonify(result)


@app.route('/analytics/confirmed/<int:month>', methods=['GET'])
def get_confirmed_slots(month: int):
    managers = session.query(Manager).all()
    total_amount = len(session.query(Slots).filter(
        Slots.status_id == 4, func.extract('month', Slots.date) == month).all())
    result = {
        'amount': total_amount,
        'managers': []
    }

    for manager in managers:
        number_of_slots = len(session.query(Slots).filter(Slots.status_id == 4, func.extract('month', Slots.date) == month, Slots.manager_id == manager.id).all())
        result['managers'].append(
            {
                'manager': manager.name,
                'number_of_slots': number_of_slots,
                'absolute_value': (number_of_slots * 100 / total_amount) if total_amount > 0 else 0
            }
        )

    result['managers'].sort(key=lambda x: x['number_of_slots'], reverse=True)
    return jsonify(result)


@app.route('/analytics/completed/success/<int:month>', methods=['GET'])
def get_successfully_completed_slots(month: int):
    managers = session.query(Manager).all()
    total_amount = len(session.query(Slots).filter(
        Slots.status_id == 7, func.extract('month', Slots.date) == month).all())
    result = {
        'amount': total_amount,
        'managers': []
    }

    for manager in managers:
        number_of_slots = len(session.query(Slots).filter(Slots.status_id == 7, func.extract('month', Slots.date) == month, Slots.manager_id == manager.id).all())
        result['managers'].append(
            {
                'manager': manager.name,
                'number_of_slots': number_of_slots,
                'absolute_value': (number_of_slots * 100 / total_amount) if total_amount > 0 else 0
            }
        )

    result['managers'].sort(key=lambda x: x['number_of_slots'], reverse=True)
    return jsonify(result)