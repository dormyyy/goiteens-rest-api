import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
def create_gc_table(table_name):
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('booking-system-391911-0c39b19a2b6c.json', scope)

    # Authenticate with the Google Sheets API
    client = gspread.authorize(credentials)
    client.create(title=table_name)


def push_to_google_sheets(response):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('booking-system-391911-0c39b19a2b6c.json', scope)

    # Authenticate with the Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    # Spreadsheet ID of the Google Sheets document
    spreadsheet_id = '1mcHfE8cg61DN1cQhoozJDadAatwhaNwoit7dRpag5E4'

    # Clear existing data in the sheet
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range='Аркуш1',
        body={}
    ).execute()

    # Write the response data to the sheet
    data = response['managers']
    values = [['Manager', 'Absolute Value', 'Number of Slots']]
    for item in data:
        values.append([
            item['manager'].strip(),
            item['absolute_value'],
            item['number_of_slots']
        ])

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Аркуш1',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()

    print("Data pushed to Google Sheets successfully.")


if __name__ == '__main__':
    create_gc_table('Scheduled_nc')