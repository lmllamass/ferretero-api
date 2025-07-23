from fastapi import FastAPI, Request
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import tempfile
import json

app = FastAPI()

# Configuración
USER_ID = "0662759feb731be6fd95c59c4bad9f5209286336"
DATERIUM_API_URL = "https://api.dateriumsystem.com/"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1ea62WcCQG4GjJx1SEBsy6Y_POy2zzrT0FJl7SpM83wg"

# Autenticación con Google Sheets
def get_google_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Cargar desde variable de entorno en producción (Railway)
    if os.getenv("GOOGLE_CREDENTIALS_JSON"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_json:
            temp_json.write(os.getenv("GOOGLE_CREDENTIALS_JSON").encode())
            temp_json.seek(0)
            return ServiceAccountCredentials.from_json_keyfile_name(temp_json.name, scope)
    
    # Opción local (si trabajas con archivo directamente)
    return ServiceAccountCredentials.from_json_keyfile_name("credenciales-local.json", scope)

# Inicializar hoja de Google
credentials = get_google_credentials()
client = gspread.authorize(credentials)
sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# Endpoint principal
@app.post("/consultar")
async def consultar_producto(request: Request):
    data = await request.json()
    producto = data.get("producto")

    if not producto:
        return {"error": "No se proporcionó el nombre del producto"}

    try:
        # Consulta a Daterium
        response = requests.get(DATERIUM_API_URL, params={"consulta": producto, "user": USER_ID})
        resultado = response.json()

        # Registro en la hoja de cálculo
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