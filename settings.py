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
    result = environ['DB_NAME']
    return result


def get_db_user_name():
    result = environ['DB_USER']
    return result


def get_db_password():
    result = environ['DB_PASS']
    return result


def get_db_host():
    result = environ['DB_HOST']
    return result


def get_db_port():
    result = environ['DB_PORT']
    return result
