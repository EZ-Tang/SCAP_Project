"""
Author: Eric Tang
Date: 11/28/2021
SCAP Project V1.0
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("SCAP").worksheet("nvd_type")
sheet.clear()  
sheet = client.open("SCAP").worksheet("nvd_data")
sheet.clear()  
sheet = client.open("SCAP").worksheet("nvd_date")
sheet.clear()  