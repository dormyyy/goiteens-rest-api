from email import message
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, create_engine
from flask_marshmallow import Marshmallow
from utils.convert_str_to_datetime import to_datetime
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
CORS(app, supports_credentials=True)

db = create_engine('postgresql+psycopg2://yzgqehdjexidhz:37f052fecbe23a36ae0dcf8f9fcc0522f8bca4364880adb2fb2a2decb4830028@\
ec2-52-30-75-37.eu-west-1.compute.amazonaws.com/dedrifjd2m4iod')
ma = Marshmallow(app)
base = declarative_base()

Session = sessionmaker(db)  
session = Session()

@app.cli.command('db_create')
def db_create():
    base.metadata.create_all(db)
    print('Database created')  


@app.cli.command('db_drop')
def db_drop():
    base.metadata.drop_all(db)
    print('Database dropped')


# main page {

@app.route('/')
def main_page():
    return '<h1>Backend for GOITeens managemet system</h1>'

# main page }


# managers table routers {
@app.route('/register_manager', methods=['POST'])
def create_manager():
    name = request.form['name']
    test = session.query(Manager).filter_by(name=name).first()
    if test:
        return jsonify(message='This manager already exist'), 409
    else:
        manager_name = request.form['name']
        description = request.form['description']
        login = request.form['login']
        password = request.form['password']
        manager = Manager(name=manager_name, description=description, login=login, password=password)
        session.add(manager)
        session.commit()
        test = session.query(Manager).filter_by(name=name).first()
        data = manager_schema.dump(test)
        return jsonify(data=data, message=f'Manager {manager.id} successfully registered'), 201


@app.route('/remove_manager/<int:manager_id>', methods=['DELETE'])
def remove_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        session.delete(manager)
        session.commit()
        return jsonify(message=f'Manager {manager.id} successfully deleted.'), 202
    else:
        return jsonify(message='Manager does not exist'), 404


@app.route('/managers', methods=['GET'])
def get_managers():
    managers_list = session.query(Manager).all()
    result = managers_schema.dump(managers_list)
    return jsonify(data=result)


@app.route('/update_manager/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id: int):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    if manager:
        for key in request.form:
            if key == 'name':
                manager.name = request.form['name']
            elif key == 'description':
                manager.description = request.form['description']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        manager = session.query(Manager).filter_by(id=manager_id).first()
        data = manager_schema.dump(manager)
        return jsonify(data=data, message=f'Manager {manager.name} successfully updated'), 202
    else:
        return jsonify(message='This manager does not exist.'), 404

# manager table routers }

# status table routers {
@app.route('/register_status', methods=['POST'])
def register_status():
    name = request.form['name']
    status = session.query(Status).filter_by(name=name).first()
    if status:
        return jsonify(message='This status already exist'), 409
    else:
        status_name = name
        status_color = request.form['color']
        status = Status(name=status_name, color=status_color)
        session.add(status)
        session.commit()
        status = session.query(Status).filter_by(name=name).first()
        data = status_schema.dump(status)
        return jsonify(data=data, message=f'Status {status.id} successfully registered'), 201


@app.route('/remove_status/<int:status_id>', methods=['DELETE'])
def remove_status(status_id: int):
    status = session.query(Status).filter_by(id=status_id).first()
    if status:
        session.delete(status)
        session.commit()
        return jsonify(message=f'Status {status.name} successfully deleted'), 202
    else:
        return jsonify(message='Status does not exist'), 404


@app.route('/statuses', methods=['GET'])
def get_statuses():
    statuses_list = session.query(Status).all()
    result = statuses_schema.dump(statuses_list)
    return jsonify(data=result)


@app.route('/update_status/<int:status_id>', methods=['PUT'])
def update_status(status_id: int):
    status = session.query(Status).filter_by(id=status_id).first()
    if status:
        for key in request.form:
            if key == 'name':
                status.name = request.form['name']
            elif key == 'color':
                status.color = request.form['color']
            else:
                return jsonify(message=f'invalid field {key}'), 404
        session.commit()
        status = session.query(Status).filter_by(id=status_id).first()
        data = status_schema.dump(status)
        return jsonify(data=data, message=f'Status {status.id} successfully updated'), 202
    else:
        return jsonify(message='This status does not exist.'), 404
# status table routers}

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
        time = request.form['time']
        slot_manager_id = request.form['manager_id']
        slot_status_id = request.form['status_id']
        if int(slot_manager_id) in [i.id for i in managers] and int(slot_status_id) in [i.id for i in statuses]:
            slot = Slots(name=slot_name, date=slot_date, time=time,
            manager_id=slot_manager_id, status_id=slot_status_id)
            session.add(slot)
            session.commit()
            slot = session.query(Slots).filter_by(name=name).first()
            data = slot_schema.dump(slot)
            return jsonify(data=data, message=f'Slot {slot.id} successfully registered'), 201
        else:
            return jsonify(message=f'Invalid manager id or status_id'), 201


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
    return jsonify(data=result)


@app.route('/update_slot/<int:slot_id>', methods=['PUT'])
def update_slot(slot_id: int):
    slot = session.query(Slots).filter_by(id=slot_id).first()
    if slot:
        for key in request.form:
            if key == 'name':
                slot.name = request.form['name']
            elif key == 'date':
                try:
                    slot_date = to_datetime(request.form['date'])
                except:
                    return jsonify(message='Invalid time format. Please match the format dd.mm.yyyy'), 404 
                finally:
                    slot.date = slot_date
            elif key == 'time':
                time = request.form['time']
                if int(time) in range(8,23):
                    slot.time = time
                else:
                    return jsonify(message='Invalid time [from 8 to 22]')
            elif key == 'manager_id':
                slot.manager_id = request.form['manager_id']
            elif key == 'status_id':
                slot.status_id = request.form['status_id']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        slot = session.query(Slots).filter_by(id=slot_id).first()
        data = slot_schema.dump(slot)
        return jsonify(data=data, message=f'Slot {slot.id} successfully updated'), 202
    else:
        return jsonify(message='This slot does not exist'), 404
# slots table routers }

# courses table routers {
@app.route('/register_course', methods=['POST'])
def register_course():
    name = request.form['name']
    course = session.query(Course).filter_by(name=name).first()
    if course:
        return jsonify(message='This course already exist'), 409
    else:
        course_name = name
        course_description = request.form['description']
        course = Course(name=course_name, description=course_description)
        session.add(course)
        session.commit()
        course = session.query(Course).filter_by(name=name).first()
        data = course_schema.dump(course)
        return jsonify(data=data, message=f'Course {course.id} successfully registered'), 201


@app.route('/remove_course/<int:course_id>', methods=['DELETE'])
def remove_course(course_id: int):
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        session.delete(course)
        session.commit()
        return jsonify(message=f'Course {course.id} successfully deleted'), 200
    else:
        return jsonify(message='Course does not exist'), 404


@app.route('/courses', methods=['GET'])
def get_courses():
    courses_list = session.query(Course).all()
    result = courses_schema.dump(courses_list)
    return jsonify(data=result)


@app.route('/update_course/<int:course_id>', methods=['PUT'])
def update_course(course_id: int):
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        for key in request.form:
            if key == 'name':
                course.name = request.form['name']
            elif key == 'description':
                course.description = request.form['description']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        course = session.query(Course).filter_by(id=course_id).first()
        data = course_schema.dump(course)
        return jsonify(data=data, message=f'Course {course.id} successfully updated'), 202
    else:
        return jsonify(message='This course does not exist'), 404
# courses table routers }

# groups table routers {
@app.route('/register_group', methods=['POST'])
def register_group():
    name = request.form['name']
    group = session.query(Group).filter_by(name=name).first()
    courses = session.query(Course).all()
    if group:
        return jsonify(message='This group already exist'), 409
    else:
        group_name = name
        group_course_id = request.form['course_id']
        group_timetable = request.form['timetable']
        if int(group_course_id) in [i.id for i in courses]:
            group = Group(name=group_name, course_id=group_course_id, timetable=group_timetable)
            session.add(group)
            session.commit()
            group = session.query(Group).filter_by(name=name).first()
            data = group_schema.dump(group)
            return jsonify(data=data, message=f'Group {group.id} successfully registered'), 201
        else:
            return jsonify(message='Invalid course_id field.'), 404

@app.route('/remove_group/<int:group_id>', methods=['DELETE'])
def remove_group(group_id: int):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        session.delete(group)
        session.commit()
        return jsonify(message=f'Group {group.id} successfully deleted'), 200
    else:
        return jsonify(message='This group does not exist'), 404


@app.route('/groups', methods=['GET'])
def get_groups():
    groups_list = session.query(Group).all()
    result = groups_schema.dump(groups_list)
    return jsonify(data=result)


@app.route('/update_group/<int:group_id>', methods=['PUT'])
def update_group(group_id: int):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        for key in request.form:
            if key == 'name':
                group.name = request.form['name']
            elif key == 'course_id':
                group.course_id = request.form['course_id']
            elif key == 'timetable':
                group.timetable = request.form['timetable']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        group = session.query(Group).filter_by(id=group_id).first()
        data = group_schema.dump(group)
        return jsonify(data=data, message=f'Group {group.id} successfully updated'), 202
    else:
        return jsonify(message='Group does not exist'), 404
# groups table routers }

# results table routers {
@app.route('/register_result', methods=['POST'])
def register_result():
    name = request.form['name']
    test = session.query(Results).filter_by(name=name).first()
    if test:
        return jsonify(message='This result already exist'), 409
    else:
        result_name = name
        result_description = request.form['description']
        result_color = request.form['color']    
        result = Results(name=result_name, description=result_description, color=result_color)
        session.add(result)
        session.commit()
        test = session.query(Results).filter_by(name=name).first()
        data = result_schema.dump(test)
        return jsonify(data=data, message=f'Result {result.id} successfully registered.'), 202


@app.route('/remove_result/<int:result_id>', methods=['DELETE'])
def remove_result(result_id: int):
    result = session.query(Results).filter_by(id=result_id).first()
    if result:
        session.delete(result)
        session.commit()
        return jsonify(message=f'Result {result.id} successfully deleted.'), 200
    else:
        return jsonify(message='This result does not exist.'), 404


@app.route('/results', methods=['GET'])
def get_results():
    results_list = session.query(Results).all()
    result = results_schema.dump(results_list)
    return jsonify(data=result)


@app.route('/update_result/<int:result_id>', methods=['PUT'])
def update_results(result_id: int):
    result = session.query(Results).filter_by(id=result_id).first()
    if result:
        for key in request.form:
            if key == 'name':
                result.name = request.form['name']
            elif key == 'description':
                result.description = request.form['description']
            elif key == 'color':
                result.color = request.form['color']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        result = session.query(Results).filter_by(id=result_id).first()
        data = result_schema.dump(result)
        return jsonify(data=data, message=f'Result {result.id} successfully updated.'), 202
    else:
        return jsonify(message='Result does not exist.'), 404
# results table routers }

# appointments table routers {
@app.route('/register_appointment', methods=['POST'])
def register_appointment():
    name = request.form['name']
    test = session.query(Appointment).filter_by(name=name).first()
    slots = session.query(Slots).all()
    courses = session.query(Course).all()
    if test:
        return jsonify(message='This appointment already exist'), 409
    else:
        appointment_name = name
        appointment_zoho_link = request.form['zoho_link']
        appointment_slot_id = request.form['slot_id']
        appointment_course_id = request.form['course_id']
        appointment_comments = request.form['comments']
        if int(appointment_slot_id) in [i.id for i in slots] and int(appointment_course_id) in [i.id for i in courses]:
            appointment = Appointment(name=appointment_name, zoho_link=appointment_zoho_link,
            slot_id=appointment_slot_id, course_id=appointment_course_id, comments=appointment_comments)
            session.add(appointment)
            session.commit()
            test = session.query(Appointment).filter_by(name=name).first()
            data = appointment_schema.dump(test)
            return jsonify(data=data, message=f'Appointment {appointment.id} successfully registered'), 202
        else:
            return jsonify(message='Invalid field course_id or slot_id')


@app.route('/remove_appointment/<int:appointment_id>', methods=['DELETE'])
def remove_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        return jsonify(message=f'Appointment {appointment.id} successfully deleted.'), 200
    else:
        return jsonify(message='This appointment does not exist.'), 404


@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments_list = Appointment.query.all()
    result = appointments_schema.dump(appointments_list)
    return jsonify(data=result)


@app.route('/update_appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id: int):
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        for key in request.form:
            if key == 'name':
                appointment.name = request.form['name']
            elif key == 'zoho_link':
                appointment.zoho_link = request.form['zoho_link']
            elif key == 'zlot_id':
                appointment.slot_id = request.form['slot_id']
            elif key == 'course_id':
                appointment.course_id = request.form['course_id']
            elif key == 'comments':
                appointment.comments = request.form['comments']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        appointment = session.query(Appointment).filter_by(id=appointment_id).first()
        data = appointment_schema.dump(appointment)
        return jsonify(data=data, message=f'Appointment {appointment.id} successfully updated.'), 202
    else:
        return jsonify(message='Appointment does not exist'), 404
# appointments table routers }

# roles table routers {
@app.route('/register_role', methods=['POST'])
def register_role():
    name = request.form['name']
    test = session.query(Roles).filter_by(name=name).first()
    if test:
        return jsonify(message='This role already exist'), 409
    else:
        role_name = name
        role_description = request.form['description']
        role = Roles(name=role_name, description=role_description)
        session.add(role)
        session.commit()
        test = session.query(Roles).filter_by(name=name).first()
        data = role_schema.dump(test)
        return jsonify(data=data, message=f'Role {role.id} successfully registered'), 202


@app.route('/remove_role/<int:role_id>', methods=['DELETE'])
def remove_role(role_id: int):
    role = session.query(Roles).filter_by(id=role_id).first()
    if role:
        session.delete(role)
        session.commit()
        return jsonify(message=f'Role {role.id} successfully deleted.'), 200
    else:
        return jsonify(message='This role does not exist'), 404


@app.route('/roles', methods=['GET'])
def get_roles():
    roles_list = session.query(Roles).all()
    result = roles_schema.dump(roles_list)
    return jsonify(data=result)


@app.route('/update_role/<int:role_id>', methods=['PUT'])
def update_role(role_id: int):
    role = session.query(Roles).filter_by(id=role_id).first()
    if role:
        for key in request.form:
            if key == 'name':
                role.name = request.form['name']
            elif key == 'description':
                role.description = request.form['desctiption']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        role = session.query(Roles).filter_by(id=role_id).first()
        data = role_schema.dump(role)
        return jsonify(data=data, message=f'Role {role.id} successfully updated.'), 202
    else:
        return jsonify(message='Role does not exist'), 404
# roles table routers }

# users table routers {
@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    test = session.query(Users).filter_by(name=name).first()
    roles = session.query(Roles).all()
    if test:
        return jsonify(message='This user already exist'), 409
    else:
        user_name = name
        user_description = request.form['description']
        user_login = request.form['login']
        user_password = request.form['password']
        user_role_id = request.form['role_id']
        if int(user_role_id) in [i.id for i in roles]:
            user = Users(name=user_name, description=user_description,
            login=user_login, password=user_password, role_id=user_role_id)
            session.add(user)
            session.commit()
            test = session.query(Users).filter_by(name=name).first()
            data = user_schema.dump(test)
            return jsonify(data=data, message=f'User {user.id} successfully registered'), 202
        else:
            return jsonify(message='Invalid role_id field'), 404


@app.route('/remove_user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id: int):
    user = session.query(Users).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return jsonify(message=f'User {user.id} successfully deleted.'), 200
    else:
        return jsonify(message='This user does not exist'), 404


@app.route('/users', methods=['GET'])
def get_users():
    users_list = session.query(Users).all()
    result = users_schema.dump(users_list)
    return jsonify(data=result)


@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    user = session.query(Users).filter_by(id=user_id).first()
    if user:
        for key in request.form:
            if key == 'name':
                user.name = request.form['name']
            elif key == 'description':
                user.description = request.form['description']
            elif key == 'login':
                user.login = request.form['login']
            elif key == 'password':
                user.login = request.form['password']
            elif key == 'role_id':
                user.role_id = request.form['role_id']
            else:
                return jsonify(message=f'Invalid field {key}'), 404
        session.commit()
        user = session.query(Users).filter_by(id=user_id).first()
        data = user_schema.dump(user)
        return jsonify(data=data, message=f'User {user.id} successfully updated.'), 202
    else:
        return jsonify(message='User does not exist'), 404
# users table routers }



# db models
class Manager(base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(150))
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


class Status(base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    color = Column(String(50))


class Slots(base):
    __tablename__ = 'slots'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey(Manager.id, ondelete='SET DEFAULT'), default=0)
    status_id = Column(Integer, ForeignKey(Status.id, ondelete='SET DEFAULT'), default=0)


class Course(base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)


class Group(base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id, ondelete='SET DEFAULT'), default=0)
    name = Column(String(80), nullable=False)
    timetable = Column(Text)


class Results(base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String(50))


class Appointment(base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    zoho_link = Column(Text)
    slot_id = Column(Integer, ForeignKey(Slots.id, ondelete='SET DEFAULT'), default=0)
    course_id = Column(Integer, ForeignKey(Course.id, ondelete='SET DEFAULT'), default=0)
    name = Column(String(150), nullable=False)
    comments = Column(Text)


class Roles(base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)


class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey(Roles.id, ondelete='SET DEFAULT'), default=0)

class ManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'login', 'password')


class StatusesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'color')


class SlotsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'date', 'time', 'manager_id', 'status_id')


class CoursesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class GroupsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'course_id', 'name', 'timetable')


class ResultsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'color')

    
class AppointmentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'zoho_link', 'slot_id', 'course_id', 'name', 'comments')


class RolesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'login', 'password', 'role_id')


manager_schema = ManagerSchema()
status_schema = StatusesSchema()
slot_schema = SlotsSchema()
course_schema = CoursesSchema()
group_schema = GroupsSchema()
result_schema = ResultsSchema()
appointment_schema = AppointmentsSchema()
role_schema = RolesSchema()
user_schema = UsersSchema()

managers_schema = ManagerSchema(many=True)
statuses_schema = StatusesSchema(many=True)
slots_schema = SlotsSchema(many=True)
courses_schema = CoursesSchema(many=True)
groups_schema = GroupsSchema(many=True)
results_schema = ResultsSchema(many=True)
appointments_schema = AppointmentsSchema(many=True)
roles_schema = RolesSchema(many=True)
users_schema = UsersSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)