import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from app import app, session
from models import *
from datetime import date, datetime


last_backup = '2022-09-19'
last_backup = datetime.strptime(last_backup, '%Y-%m-%d')
table = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J',
    11: 'K',
    12: 'L'
}


def push(service, data, table_name, spreadsheet_id):
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f'{table_name}!A2:{table.get(len(data[0]))}{2 + len(data)}',
             "majorDimension": "ROWS",
             "values": data}
        ]
    }).execute()


def backup():
    global last_backup
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'creds.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = '1U9hUeD3nFYSLOOFRgwXDFPLayqTMToixg6Y5KB7zhuI'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    if (datetime.today() - last_backup).days > 0:
        last_backup = datetime.today()
        # tmp
        # statuses = [[str(status.id), status.name, status.color] for status in session.query(Status).all()]
        # roles = [[str(role.id), role.name, role.description] for role in session.query(Roles).all()]
        # templates = [[str(template.id), str(template.manager_id), template.template, str(template.saved_date)] for template in session.query(Templates).all()]
        # tmp
        managers = [[str(manager.id), manager.name, manager.telegram, manager.login,
                     manager.password] for manager in session.query(Manager).all()]

        users = [[str(user.id), user.name, user.telegram, user.login, user.password,
                  str(user.role_id)] for user in session.query(Users).all()]

        work_weeks = [[str(week.id), str(week.date_start), str(week.date_finish)] for week in session.query(Weeks).all()]

        slots = [[str(slot.id), slot.name, str(slot.date), str(slot.time),
                  str(slot.manager_id), str(slot.status_id), str(slot.week_day)] for slot in session.query(Slots).all()]

        appointments = [[str(appointment.id), appointment.zoho_link, str(appointment.slot_id), str(appointment.course_id),
                         str(appointment.age), appointment.phone, str(appointment.group_id), appointment.comments,
                         str(appointment.cancel_type)] for appointment in session.query(Appointment).all()]

        groups = [[str(group.id), str(group.course_id), group.name,
                   group.timetable] for group in session.query(Group).all()]

        courses = [[str(course.id), course.name, course.description] for course in session.query(Course).all()]

        push(service, work_weeks, 'work_weeks', spreadsheet_id)
        push(service, managers, 'managers', spreadsheet_id)
        push(service, users, 'users', spreadsheet_id)
        push(service, slots, 'slots', spreadsheet_id)
        push(service, appointments, 'appointments', spreadsheet_id)
        push(service, groups, 'groups', spreadsheet_id)
        push(service, courses, 'courses', spreadsheet_id)
        # tmp
        # push(service, statuses, 'statuses', spreadsheet_id)
        # push(service, roles, 'roles', spreadsheet_id)
        # push(service, templates, 'templates', spreadsheet_id)
        # tmp
