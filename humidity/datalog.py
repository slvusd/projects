from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Set up credentials (you'll need to handle authentication)
#creds = Credentials.from_authorized_user_file('/home/pi/cred.json', ['https://www.googleapis.com/auth/spreadsheets'])
creds = Credentials.from_service_account_file(
    '/home/pi/cred.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)


# Create the Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Specify the spreadsheet ID and range
spreadsheet_id = '1rwSCWixjr1DTLtRIu-gIft9fmEpuEOblL2FRSd4E3Z0'
range_ = 'Sheet1!A:A'  # Adjust this to your sheet name and desired range

# Prepare the values to append
values = [
    ['New', 'Row', 'Data'],
    # Add more rows as needed
]

body = {
    'values': values
}

# Append the values
result = service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range=range_,
    valueInputOption='USER_ENTERED',
    body=body
).execute()

print(f"{result.get('updates').get('updatedCells')} cells appended.")

