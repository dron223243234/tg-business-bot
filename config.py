import os
from dotenv import load_dotenv as ld

ld()
token = os.getenv('BOT_TOKEN')
admin = os.getenv('ADMIN_ID', 0)

if not token or not admin:
    exit('Ошибка: нет BOT_TOKEN или ADMIN_ID')

