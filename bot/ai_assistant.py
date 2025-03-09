import openai
import os
import time
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Подключаем OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Храним треды для пользователей (чтобы ассистент запоминал контекст)
user_threads = {}

def get_ai_response(user_id, user_message):
    """
    Отправляет сообщение ассистенту OpenAI и получает ответ.
    """

    # Если у пользователя нет треда, создаём новый
    if user_id not in user_threads:
        thread = client.beta.threads.create()
        user_threads[user_id] = thread.id

    thread_id = user_threads[user_id]

    # Отправляем сообщение ассистенту
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Запускаем ассистента на этом треде
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Ожидаем завершения обработки
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)  # Ждём 1 секунду перед проверкой статуса

    # Получаем ответ от ассистента
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            return msg.content[0].text.value  # Возвращаем текст ответа

    return "Ошибка: ассистент не дал ответа."
