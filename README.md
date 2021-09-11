# weather_bot
Бот погоды для telegram
Для запуска необходимо токен передать переменной при запуске контейнера, либо вставить в Docker-compose

Docker:

//сборка docker image
docker build -t my-python-bot .

//создание и запуск docker container из docker image
docker run -d --restart=always --name my-bot --env BOT_TOKEN='токен бота без ковычек' my-python-bot


Docker-compose:
insert BOT_TOKEN in yml-file
docker-compose up -d

 
# bot.token
передать переменной при запуске кастомного контейнера BOT_TOKEN=
