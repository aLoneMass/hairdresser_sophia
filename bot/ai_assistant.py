import openai
import os
from dotenv import load_dotenv

# Загружаем ключи из .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_ItEAZFii2xydD7Yh2SZi6TIU"

# Подключаем OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Создаём сессию (тред) для каждого пользователя
user_threads = {}

def get_ai_response(user_id, user_message):
    # Создаём новый тред, если его ещё нет
    if user_id not in user_threads:
        thread = client.beta.threads.create()
        user_threads[user_id] = thread.id
    else:
        thread_id = user_threads[user_id]

    # Отправляем сообщение ассистенту
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Запрашиваем ответ от ассистента
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Ожидаем завершения обработки (можно улучшить через WebSocket)
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break

    # Получаем ответ от ассистента
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            return msg.content[0].text.value  # Возвращаем текст ответа

    return "Ошибка при получении ответа от ассистента."
