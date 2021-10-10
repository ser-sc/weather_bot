import psycopg2
from settings import get_db_name, get_db_user_name, get_db_password, get_db_host, get_db_port


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

    def __execute_read_query_all(self, query: str, parameters: dict = None):
        try:
            self.__cursor.execute(query, parameters)
            result = self.__cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Rollback transaction. The error '{error}' occurred.")
            self.__connection.rollback()

    def __execute_read_query_one(self, query: str, parameters: dict = None):
        try:
            self.__cursor.execute(query, parameters)
            result = self.__cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Rollback transaction. The error '{error}' occurred.")
            self.__connection.rollback()

    def __execute_insert_query_one(self, query: str, parameters: dict = None):
        try:
            self.__cursor.execute(query, parameters)
            self.__connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Rollback transaction. The error '{error}' occurred.")
            self.__connection.rollback()

    def get_city_id_db(self, city_name: str):
        query = "select city_id from city where lower(name) = %(city_name)s;"
        parameter = {'city_name': city_name.lower(), }
        city_id = self.__execute_read_query_one(query, parameter)
        if city_id is not None:
            result = str(city_id[0])
        else:
            result = False
        return result

    def get_dict_of_city_db(self):
        query = "select name, city_id from city order by name;"
        all_city = self.__execute_read_query_all(query)
        result = dict(all_city)
        return result

    def check_chat_id_db(self, chat_id: int):
        query = "select exists (select * from favourite where chat_id = %(chat_id)s);"
        parameter = {'chat_id': chat_id, }
        result = self.__execute_read_query_one(query, parameter)[0]
        return result

    def check_city_in_favourite_db(self, chat_id: int, city_id: int):
        query = "select exists (select * from favourite " \
                "where chat_id = %(chat_id)s " \
                "and city_id = %(city_id)s);"
        parameter = {'chat_id': chat_id, 'city_id': city_id, }
        result = self.__execute_read_query_one(query, parameter)[0]
        return result

    def get_favourite_list_db(self, chat_id: int):
        query = "select city.name, city.city_id from favourite fav " \
                "join city on city.city_id = fav.city_id " \
                "where fav.chat_id = %(chat_id)s " \
                "order by city.name;"
        parameter = {'chat_id': chat_id, }
        favourite_list = self.__execute_read_query_all(query, parameter)
        result = dict(favourite_list)
        return result

    def set_default_favourite_list_db(self, chat_id: int):
        insert_query = "insert into favourite (chat_id, city_id) values" \
                       "(%(chat_id)s, 59828)," \
                       "(%(chat_id)s, 76628)," \
                       "(%(chat_id)s, 622578)," \
                       "(%(chat_id)s, 72223)," \
                       "(%(chat_id)s, 17920);"
        parameter = {'chat_id': chat_id, }
        self.__execute_insert_query_one(insert_query, parameter)

    def set_city_to_favourite_db(self, chat_id: int, city_id: int):
        insert_query = "insert into favourite (chat_id, city_id) values" \
                       "(%(chat_id)s, %(city_id)s) " \
                       "on conflict (chat_id, city_id) " \
                       "do nothing;"
        parameter = {'chat_id': chat_id, 'city_id': city_id, }
        self.__execute_insert_query_one(insert_query, parameter)

    def del_city_from_favourite_db(self, chat_id: int, city_id: int):
        insert_query = "delete from favourite " \
                       "where chat_id = %(chat_id)s " \
                       "and city_id = %(city_id)s;"
        parameter = {'chat_id': chat_id, 'city_id': city_id, }
        self.__execute_insert_query_one(insert_query, parameter)

