from fastapi import FastAPI, Request
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

app = FastAPI()

# CONFIGURACIÓN
USER_ID = "0662759feb731be6fd95c59c4bad9f5209286336"
DATERIUM_API = "https://api.dateriumsystem.com/"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ea62WcCQG4GjJx1SEBsy6Y_POy2zzrT0FJl7SpM83wg"
CREDENCIALES_JSON = "/Users/lmllamas/Library/Mobile Documents/com~apple~CloudDocs/konkabeza/compra-inteligente-konkabeza-f083d528b672.json"  # Cambia si tu archivo se llama diferente

# AUTENTICACIÓN CON GOOGLE SHEETS
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENCIALES_JSON, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# ENDPOINT PRINCIPAL
@app.post("/consultar")
async def consultar_producto(request: Request):
    data = await request.json()
    producto = data.get("producto")

    if not producto:
        return {"error": "No se proporcionó producto"}

    # Llamar a Daterium
    try:
        response = requests.get(
            DATERIUM_API,
            params={"consulta": producto, "user": USER_ID}
        )

        resultado = response.json()

        # Guardar en Google Sheets
        sheet.append_row([
            datetime.now().isoformat(),
            producto,
            json.dumps(resultado, ensure_ascii=False)
        ])

        return {
            "producto": producto,
            "resultado": resultado
        }

    except Exception as e:
        return {"error": str(e)}