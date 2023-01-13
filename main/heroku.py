import os

AllOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = True

def set_heroku_settings():
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']