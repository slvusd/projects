#!/usr/bin/env python
# Eric Brown 27 Nov 2024
# From: https://github.com/adafruit/Adafruit_CircuitPython_AHTx0

import time
from datetime import datetime
import board
import adafruit_ahtx0

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

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

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

# Current timestamp formatted as string
now = datetime.now()
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date = now.strftime("%Y-%m-%d")
tim = now.strftime("%H:%M:%S")

def c2f(c):
    """
    Convert Celsius to Fahrenheit.
    
    Args:
    celsius (float): Temperature in Celsius
    
    Returns:
    float: Temperature in Fahrenheit
    """
    return (c * 9/5) + 32

while True:
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    tim = now.strftime("%H:%M:%S")
    t = f'=DATEVALUE("{date}") + TIMEVALUE("{tim}")'
    c = sensor.temperature
    f = c2f(c)
    h = sensor.relative_humidity

    values = [
            [ t, c, f, h ]
    ]
    body = { 'values': values }

    # Append the values
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    #print(f"Temperature: {sensor.temperature:.1f}°C/{c2f(sensor.temperature):.1f}°F Humidity: {sensor.relative_humidity:.1f}%")
    #print(values)
    time.sleep(600)
