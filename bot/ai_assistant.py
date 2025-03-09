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

# Храним треды пользователей
user_threads = {}

def get_ai_response(user_id, user_message):
    """
    Отправляет сообщение ассистенту OpenAI и получает ответ.
    """

    # Создаём новый тред для пользователя, если он ещё не существует
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

    # Запускаем ассистента
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
            break  # Запрос обработан
        elif run_status.status == "requires_action":
            # Обрабатываем вызов функции ассистента
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool in tool_calls:
                if tool.function.name == "read_service_list":
                    # Возвращаем фиктивные данные об услугах
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": '{"services": ["Маникюр", "Педикюр", "Окрашивание волос", "Массаж"]}'
                    })

            # Отправляем результат OpenAI
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run_status.status in ["failed", "cancelled"]:
            return "❌ Ошибка: ассистент не смог обработать запрос."

        time.sleep(2)

    # Получаем ответ ассистента
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            return msg.content[0].text.value  # Возвращаем ответ ассистента

    return "❌ Ошибка: ассистент не дал ответа."
