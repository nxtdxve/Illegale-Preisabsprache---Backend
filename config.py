import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY = os.environ.get('API_KEY')
    MAILTRAP_TOKEN = os.environ.get('MAILTRAP_TOKEN')
    SCHEDULER_API_ENABLED = True
