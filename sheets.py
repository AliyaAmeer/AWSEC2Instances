# sheets.py

from __future__ import print_function
from auth import spreadsheet_service
from auth import drive_service

def create():
    spreadsheet_details = {
    'properties': {
        'title': 'EC2 Instances'
        }
    }
    sheet = spreadsheet_service.spreadsheets().create(body=spreadsheet_details,
                                    fields='spreadsheetId').execute()
    sheetId = sheet.get('spreadsheetId')
    print('Spreadsheet ID: {0}'.format(sheetId))
    permission1 = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': 'aliyaameer1993@gmail.com'
    }
    drive_service.permissions().create(fileId=sheetId, body=permission1).execute()
    return sheetId
    

def add_sheet(_service, _spreadsheetID, _sheetName):
    data = {'requests': [
        {
            'addSheet':{
                'properties':{'title': '{0}'.format(_sheetName)}
            }
        }
    ]}

    # Execute request
    res = spreadsheet_service.spreadsheets().batchUpdate(spreadsheetId=_spreadsheetID, body=data).execute()