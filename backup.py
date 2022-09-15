from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from utils import data_to_json
from app import app, session
from flask import request, jsonify
from models import *
from schemas import *
import json

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

    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheetList = spreadsheet.get('sheets')
    sheets_id = {
        'manager': ''
    }

    managers = [[str(manager.id), manager.name, manager.telegram, manager.login, manager.password] for manager in session.query(Manager).all()]
    users = [[str(user.id), user.name, user.telegram, user.login, user.password, str(user.role_id)] for user in session.query(Users).all()]
    work_weeks = [[str(week.id), str(week.date_start), str(week.date_finish)] for week in session.query(Weeks).all()]
    push(service, work_weeks, 'work_weeks', spreadsheet_id)
    push(service, managers, 'managers', spreadsheet_id)
    push(service, users, 'users', spreadsheet_id)


backup()
