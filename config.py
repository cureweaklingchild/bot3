import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")