#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;

  \connect $APP_DB_NAME $APP_DB_USER
  BEGIN;

    CREATE TABLE IF NOT EXISTS city (
      city_id		integer PRIMARY KEY,
      name		VARCHAR UNIQUE
    );

    CREATE UNIQUE INDEX name_lower_key ON city ((lower(name)));

    CREATE TABLE IF NOT EXISTS favourite (
      chat_id		bigint,
      city_id		integer,
      PRIMARY KEY (chat_id, city_id),
      CONSTRAINT fk_city_id
        FOREIGN KEY(city_id)
          REFERENCES city(city_id)
    );

    COMMENT ON TABLE city IS 'Справочник названий городов и ссылок на данные о погоде';
    COMMENT ON COLUMN city.city_id IS 'ИД города, первичный ключ, используется <ID> из https://meteo7.ru/forecast/<ID>';
    COMMENT ON COLUMN city.name IS 'Имя города, должно быть уникальным';
    COMMENT ON TABLE favourite IS 'Справочник скписка Избранных городов, которые будут в присутстввать в клавиатуре';
    COMMENT ON COLUMN favourite.chat_id IS 'ИД чата пользователя, для которого работает этот список Избранных городов';
    COMMENT ON COLUMN favourite.city_id IS 'ИД города, внешний ключ к таблице city';

  COMMIT;
EOSQL