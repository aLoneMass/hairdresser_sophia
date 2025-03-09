import gspread
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Файл с учетными данными OAuth
CREDENTIALS_FILE = "/opt/telegram_bots/hairdresser_sophia/client_secret_722540990069-rj20hk64r3tqqel1nldea0b659689na6.apps.googleusercontent.com.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def authenticate_google():
    """
    Авторизация через OAuth 2.0 и сохранение токена.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)  # Откроет браузер для авторизации
    return creds

def get_services():
    """
    Читает список услуг из Google Таблицы.
    """
    creds = authenticate_google()
    client = gspread.authorize(creds)

    # Замените на ваш Spreadsheet ID
    SHEET_ID = "1zMoBFXK8lhPOMWreRSRDGGIaotOYerRP8QpyxiCE-z0"
    sheet = client.open_by_key(SHEET_ID).sheet1  # Открываем первый лист

    data = sheet.get_all_records()  # Читаем данные

    services = []
    for row in data:
        services.append(
            f"📌 *{row['Название']}*\n💬 {row['Описание']}\n💰 Цена: {row['Стоимость']} руб.\n⏳ Время: {row['Временной слот']} мин\n"
        )

    return "\n\n".join(services) if services else "В таблице пока нет услуг."
