import json
from os import getenv
from typing import Optional

import gspread
from deta import Drive


KEY_FILE = getenv('GOOGLE_KEY_FILE', '')
SHEET_NAME = getenv('GOOGLE_SHEET_NAME')
WORKSHEET_NAME = getenv('GOOGLE_WORKSHEET_NAME')


def update_statistic_table(data: list[list[str]]) -> Optional[str]:
    drive = Drive('config')
    google_secret_file = drive.get(KEY_FILE)

    if not google_secret_file:
        return
        
    google_secret = json.loads(google_secret_file.read())

    try:
        service = gspread.service_account_from_dict(google_secret)
        sheet = service.open(SHEET_NAME)
        worksheet = sheet.worksheet(WORKSHEET_NAME)

        worksheet.update('A1', data)

        sheet_url: Optional[str] = sheet.url 
    except:
        sheet_url = None
    
    return sheet_url

