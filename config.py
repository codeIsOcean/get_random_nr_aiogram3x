from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN is None:
    raise ValueError('Токен Бота не определен. Проверь .env файл')
