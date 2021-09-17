from os import environ


# Модуль получения параметров среды окружения
#
# @author PopikAP87, created on 18.09.2021

def get_token():
    result = environ['BOT_TOKEN']
    return result


def get_weather_source():
    result = environ['WEATHER_SOURCE']
    return result


def get_db_name():
    result = environ['POSTGRES_DB']
    return result


def get_db_user_name():
    result = environ['POSTGRES_USER']
    return result


def get_db_password():
    result = environ['POSTGRES_PASSWORD']
    return result


def get_db_host():
    result = environ['DATABASE_HOST']
    return result


def get_db_port():
    result = environ['DATABASE_PORT']
    return result
