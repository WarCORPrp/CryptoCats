from pyrogram import Client, filters
import openai

# Установка API ключа OpenAI и настройка URL
openai.api_key = 'sk-hPu0wlDuALQCiVmkDf3d6cCaE902432e8277Bf98C036731f'
url = 'https://neuroapi.host/v1'
openai.api_base = url

app = Client("Karinya4884", api_id="22992909", api_hash="e01b980663456e120ed1cf9811ea2508")

# Хранилище контекста для каждого пользователя
context = {}

@app.on_message(filters.text & filters.private)
def handle(client, message):
    user_id = message.from_user.id

    # Инициализация контекста для пользователя
    if user_id not in context:
        context[user_id] = [{"role": "system", "content": "Ты - профессиональный таролог. Знаешь карты и их расклады. Я задаю тебе вопрос, а ты делаешь на него расклад таро "}]

    # Добавление сообщения пользователя в контекст
    context[user_id].append({"role": "user", "content": message.text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=context[user_id]
    )

    # Отправка ответа назад в чат Telegram
    chat_message = response['choices'][0]['message']['content']
    message.reply_text(chat_message)

    # Сохранение ответа в контексте
    context[user_id].append({"role": "assistant", "content": chat_message})

if __name__ == "__main__":
    app.run()