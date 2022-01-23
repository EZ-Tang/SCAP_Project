"""
Author: Eric Tang
Date: 11/21/2021
SCAP Project

Updated: 1/12/2022
"""

import gspread
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials

# opens up worksheet "SCAP"
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("SCAP")

# returns all values in a given sheet
def get_values(name, gheader = ""):
    if gheader:
        col_num = (sheet.worksheet(name).get_all_values()[0]).index(gheader)
        return sheet.worksheet(name).col_values(col_num + 1)
    return sheet.worksheet(name).get_all_values()

# TODO finish update
def update(name, values):
    sheet.worksheet(name).add_rows(1)    
    sheet.values_update(name + '!A' + str(len(get_values(name))), params={'valueInputOption': 'RAW'}, body={'values': values})

# combines two list matrices into one
def combine_nvd(nvd1, nvd2):
    nparr1 = np.array(nvd1)
    nparr2 = np.array(nvd2)
    nplist = np.append(nparr1, nparr2, axis=1)
    nplist = nplist.tolist()
    return nplist

# obtains nvd data sets from columns a to b
def split_nvd(nvd_list, a, b):
    nplist = np.array(nvd_list, dtype=object)
    nplist = nplist[:,a:b]
    nplist = nplist.tolist()
    return nplist




def feed_nvd(keys, values):
    sheet.values_update('nvd_type!A1', params={'valueInputOption': 'RAW'}, body={'values': [keys[0:10]]})
    sheet.values_update('nvd_data!A1', params={'valueInputOption': 'RAW'}, body={'values': [keys[14:27]]})
    sheet.values_update('nvd_date!A1', params={'valueInputOption': 'RAW'}, body={'values': [keys[10:14]]})



    #Splits up the data since Google Sheets can't take that much at once
    y = 2
    while values:
        sheet.worksheet("nvd_type").add_rows(1)
        sheet.worksheet("nvd_data").add_rows(1)
        sheet.worksheet("nvd_date").add_rows(1)
        if len(values) > 50000:
            sheet.values_update('nvd_type!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:50000], 0, 10)})
            sheet.values_update('nvd_data!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:50000], 14, 27)})
            sheet.values_update('nvd_date!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:50000], 10, 14)})        
            del values[:50000]
            y = y + 50000
        else:
            sheet.values_update('nvd_type!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:len(values)], 0, 10)})  
            sheet.values_update('nvd_data!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:len(values)], 14, 27)})
            sheet.values_update('nvd_date!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': split_nvd(values[0:len(values)], 10, 14)})           
            del values[:]

def feed_nipc(keys, values):
    sheet.values_update('nipc_raw!A1', params={'valueInputOption': 'RAW'}, body={'values': [keys]})

    y = 2
    sheet.values_update('nipc_raw!A' + str(y), params={'valueInputOption': 'RAW'}, body={'values': values})

