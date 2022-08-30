from email.policy import default
from app import base
from sqlalchemy import *


class Manager(base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    telegram = Column(String(150), default=0)
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


class Status(base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    color = Column(String(50), default=0)


class Slots(base):
    __tablename__ = 'slots'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)
    date = Column(Date, nullable=False)
    time = Column(Integer, nullable=False)
    manager_id = Column(Integer, ForeignKey(Manager.id, ondelete='SET DEFAULT'), default=1)
    status_id = Column(Integer, ForeignKey(Status.id, ondelete='SET DEFAULT'), default=1)
    week_day = Column(Integer, nullable=False)


class Course(base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)


class Group(base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id, ondelete='SET DEFAULT'), default=1)
    name = Column(String(80), nullable=False)
    timetable = Column(Text, default=0)


class Results(base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String(50), default=0)


class Appointment(base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    zoho_link = Column(Text, default=0)
    slot_id = Column(Integer, ForeignKey(Slots.id, ondelete='SET DEFAULT'), default=0)
    course_id = Column(Integer, ForeignKey(Course.id, ondelete='SET DEFAULT'), default=1)
    age = Column(Integer, nullable=True)
    phone = Column(String(13), nullable=False)
    group_id = Column(ForeignKey(Group.id, ondelete='SET DEFAULT'), nullable=True, default=1)
    comments = Column(Text, default=0, nullable=True)
    cancel_type = Column(Integer, default=0)


class Roles(base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)


class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    telegram = Column(Text, nullable=False)
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey(Roles.id, ondelete='SET DEFAULT'), default=1)


class Actions(base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    actor_role = Column(Integer, ForeignKey(Roles.id, ondelete='SET DEFAULT'), default=1)
    actor_id = Column(Integer, ForeignKey(Roles.id, ondelete='SET DEFAULT'), default=0)
    changing_table = Column(String(50), nullable=True)
    query = Column(String(100), nullable=True)
    datetime = Column(DateTime, nullable=False)


class Weeks(base):
    __tablename__ = 'work_weeks'
    id = Column(Integer, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_finish = Column(Date, nullable=False)


class Templates(base):
    __tablename__ = 'week_templates'
    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey(Manager.id, ondelete='SET DEFAULT'), default=1)
    template = Column(Text, default="No template saved")
    saved_date = Column(Date, default=0)
