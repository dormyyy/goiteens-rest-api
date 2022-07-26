from email import message
import json
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
from utils.convert_str_to_datetime import to_datetime, get_current_date


@app.route('/week/register', methods=['POST'])
def register_week():
    try:
        week_start = to_datetime(request.form['date_start'])
        week_finish = to_datetime(request.form['date_finish'])
    except:
        return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404
    week = session.query(Weeks).filter_by(date_start=week_start).first()
    if week:
        return jsonify(message='This week already exist'), 409
    else:
        delta = (week_finish - week_start).days
        if delta != 6:
            return jsonify(message='Invalid dates. Week must includes 7 days'), 404
        else:
            week = Weeks(date_start=week_start, date_finish=week_finish)
            session.add(week)
            session.commit()
            week = session.query(Weeks).filter_by(date_start=week_start).first()
            data = week_schema.dump(week)
            return jsonify(data=data, message=f'Week {week.id} successfully registered'), 201
    

@app.route('/week/remove/<int:week_id>', methods=['DELETE'])
def remove_week(week_id: int):
    week = session.query(Weeks).filter_by(id=week_id).first()
    if week:
        session.delete(week)
        session.commit()
        return jsonify(message=f'Week {week.id} successfully deleted'), 200
    else:
        return jsonify(message='Week does not exist'), 404


@app.route('/weeks', methods=['GET'])
def get_weeks():
    weeks_list = session.query(Weeks).all()
    result = weeks_schema.dump(weeks_list)
    return jsonify(data=result)


@app.route('/active_week_id', methods=['GET'])
def get_active_week_id():
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
            return jsonify(week_id=current_week_id)


# @app.route('/current_week/<int:manager_id>', methods=['GET'])
# def get_current_manager_week(manager_id: int):
#     weeks = session.query(Weeks).all()
#     current_date = get_current_date()
#     for i in [i.date_start for i in weeks]:
#         if (current_date - i).days <= 7:
#             current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
#     manager = session.query(Manager).filter_by(id=manager_id).first()
#     current_week = session.query(Weeks).filter_by(id=current_week_id).first()
#     print(current_week_id)
#     if manager:
#         current_week_slots = []
#         slots = session.query(Slots).filter_by(manager_id=manager_id).all()
#         for date in [i.date for i in slots]:
#             if (date - current_week.date_start).days == 0:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 monday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             monday_list.append({i: slot.status_id})
#                         else:
#                             monday_list.append({i: 0})
#                 current_week_slots.extend(['monday:', monday_list])
#             elif (date - current_week.date_start).days == 1:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 tuesday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             tuesday_list.append({i: slot.status_id})
#                         else:
#                             tuesday_list.append({i: 0})
#                 current_week_slots.extend([tuesday_list])
#             elif (date - current_week.date_start).days == 2:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 wednesday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             wednesday_list.append({i: slot.status_id})
#                         else:
#                             wednesday_list.append({i: 0})
#                 current_week_slots.extend(['wednesday:', wednesday_list])
#             elif (date - current_week.date_start).days == 3:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 thursday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             thursday_list.append({i: slot.status_id})
#                         else:
#                             thursday_list.append({i: 0})
#                 current_week_slots.extend(['thursday:', thursday_list])
#             elif (date - current_week.date_start).days == 4:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 friday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             friday_list.append({i: slot.status_id})
#                         else:
#                             friday_list.append({i: 0})
#                 current_week_slots.extend(['friday:', friday_list])
#             elif (date - current_week.date_start).days == 5:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 saturday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             saturday_list.append({i: slot.status_id})
#                         else:
#                             saturday_list.append({i: 0})
#                 current_week_slots.extend(['saturday:', saturday_list])
#             elif (date - current_week.date_start).days == 6:
#                 slots_by_date = session.query(Slots).filter_by(date=date).all()
#                 sunday_list = []
#                 for slot in slots_by_date:
#                     for i in range(8, 23):
#                         if i == slot.time:
#                             sunday_list.append({i: slot.status_id})
#                         else:
#                             sunday_list.append({i: 0})
#                 current_week_slots.extend(['sunday:', sunday_list])
#         return jsonify(active_week_id=current_week_id, manager_id=manager_id, slots=current_week_slots)


@app.route('/current_week/<int:manager_id>', methods=['GET'])
def get_current_manager_week(manager_id: int):
    weeks = session.query(Weeks).all()
    current_date = get_current_date()
    for i in [i.date_start for i in weeks]:
        if (current_date - i).days <= 7:
            current_week_id = session.query(Weeks).filter_by(date_start=i).first().id
    manager = session.query(Manager).filter_by(id=manager_id).first()
    current_week = session.query(Weeks).filter_by(id=current_week_id).first()     
    if manager:
        all_manager_slots = session.query(Slots).filter_by(manager_id=manager_id).all()
        current_week_slots = [i for i in all_manager_slots if (i.date - current_week.date_start).days <= 7]
        print(current_week_slots)
        monday_slots = []
        tuesday_slots = []
        wednesday_slots = []
        thursday_slots = []
        friday_slots = []
        saturday_slots = []
        sunday_slots = []
        result = []
        for slot in current_week_slots:
            print(slot)
            if slot.week_day == 0:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        monday_slots.append({i: slot.status_id})
                    else:
                        monday_slots.append({i: 0})
            if slot.week_day == 1:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        tuesday_slots.append({i: slot.status_id})
                    else:
                        tuesday_slots.append({i: 0})
            if slot.week_day == 2:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        wednesday_slots.append({i: slot.status_id})
                    else:
                        wednesday_slots.append({i: 0})
            if slot.week_day == 3:
                print(slot.name, slot.week_day, slot.time)
                for i in range(8,23):
                    if slot.time != i:
                        thursday_slots + (i, 0)
                    else:
                        thursday_slots + (i, slot.status_id)
                    
            if slot.week_day == 4:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        friday_slots.append({i: slot.status_id})
                    else:
                        friday_slots.append({i: 0})
            if slot.week_day == 5:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        saturday_slots.append({i: slot.status_id})
                    else:
                        saturday_slots.append({i: 0})
            if slot.week_day == 6:
                print(slot.name, slot.week_day)
                for i in range(8,23):
                    if slot.time == i:
                        sunday_slots.append({i: slot.status_id})
                    else:
                        sunday_slots.append({i: 0})

        def check_for_template(list):
            template = [[{i: 0} for i in range(8,23)]]

            if len(list) == 0:
                list = template

        for i in [monday_slots, tuesday_slots, wednesday_slots, thursday_slots, friday_slots, saturday_slots, sunday_slots]:
            check_for_template(i)
            result.extend([i])

        return jsonify(message='ok', monday=monday_slots,
        tuesday=tuesday_slots,
        wednesday=wednesday_slots,
        thursday=thursday_slots,
        friday=friday_slots,
        saturday=saturday_slots,
        sunday=sunday_slots), 200