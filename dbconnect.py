import psycopg2
from settings import get_weather_source, get_db_name, get_db_user_name, get_db_password, get_db_host, get_db_port


# Модуль установки конекшена с БД и выполнения запросов
# Соединение с БД создается при создании экземпляра класса Database
# Каждый конкретный запрос к БД выполняется в отдельной функции класса Database
# Для самих запросов к БД используются внутренние функции - помечены __ перед именем функции
#
# @author PopikAP87, created on 18.09.2021

class Database:
    def __init__(self, db_name=get_db_name(), db_user=get_db_user_name(),
                 db_password=get_db_password(), db_host=get_db_host(), db_port=get_db_port()):
        try:
            self.__connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            self.__cursor = self.__connection.cursor()
            print("Connection to PostgreSQL DB successful")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f" Lost connection. The error '{error}' occurred.")

    def __execute_read_query(self, query, parameters=None):
        try:
            self.__cursor.execute(query, parameters)
            result = self.__cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Rollback transaction. The error '{error}' occurred.")
            self.__connection.rollback()

    def get_city_link_db(self, city_name):
        query = "select city_id from city where name = %(city_name)s;"
        parameter = {'city_name': city_name, }
        city_link_id = self.__execute_read_query(query, parameter)
        result = get_weather_source() + str(city_link_id[0][0])
        return result

    def get_dict_of_city_db(self):
        query = "select name, city_id from city;"
        all_city = self.__execute_read_query(query)
        result = dict(all_city)
        return result
