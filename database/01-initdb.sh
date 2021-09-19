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

    COMMENT ON TABLE city IS 'Справочник названий городов и ссылок на данные о погоде';
    COMMENT ON COLUMN city.city_id IS 'ИД города, первичный ключ, используется <ID> из https://meteo7.ru/forecast/<ID>';
    COMMENT ON COLUMN city.name IS 'Имя города, должно быть уникальным';

    --Устанавливаем значения по умолчанию.
    --Значения повторяют те, что были в файле city.txt из предыдущей версии
    INSERT INTO
      city (city_id, name)
    VALUES
      (59828,'МШИНСКАЯ'),
      (76628,'ПРИМОРСК'),
      (622578,'ПОБЕДА'),
      (72223,'ПЕТРОЗАВОДСК'),
      (17920,'ВЫБОРГ')
    ON CONFLICT (city_id)
    DO NOTHING;

  COMMIT;
EOSQL