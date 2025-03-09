import gspread
import json
from google.oauth2.service_account import Credentials

# Файл с учетными данными OAuth
CREDENTIALS_FILE = "/opt/telegram_bots/hairdresser_sophia/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly",
          "https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/drive"]
SHEET_ID = "1zMoBFXK8lhPOMWreRSRDGGIaotOYerRP8QpyxiCE-z0" # Замените на ваш Spreadsheet ID

def get_service_names():
    """
    Получает только список уникальных услуг из Google Таблицы.
    """
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)

    # Открываем таблицу
    sheet = client.open_by_key(SHEET_ID).sheet1  

    data = sheet.get_all_records()  # Читаем данные
    services = set(row["Название"] for row in data)  # Убираем дубликаты

    return "\n".join(f"✅ {service}" for service in sorted(services))  # Красиво форматируем список

