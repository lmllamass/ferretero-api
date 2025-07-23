import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/lmllamas/Library/Mobile Documents/com~apple~CloudDocs/konkabeza/compra-inteligente-konkabeza-9ce5c0798421.json", scope)
client = gspread.authorize(creds)


# Abre por URL (reemplaza con la tuya si cambia)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1ea62WcCQG4GjJx1SEBsy6Y_POy2zzrT0FJl7SpM83wg/edit?usp=sharing")
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1ea62WcCQG4GjJx1SEBsy6Y_POy2zzrT0FJl7SpM83wg")
sheet = spreadsheet.sheet1  # Primera hoja (Worksheet)

sheet.append_row([
    datetime.now().isoformat(),
    "Tornillo DIN 912 M6x25",
    "Precio: 0,13€ - Stock: Alto"
])
sheet.append_row([
    datetime.now().isoformat(),
    "Tornillo DIN 912 M6x25",
    "Precio: 0,13€ - Stock: Alto"
])