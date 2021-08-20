# weather_bot
Бот погоды для telegram
Для запуска необходимо токен передать переменной при запуске контейнера, либо вставить в Docker-compose

Docker:
docker build -t my-python-bot .
docker run -d --rm --name my-running-app my-python-bot -v BOT_TOKEN=''
docker run --restart=always -d my-python-bot

Docker-compose
insert BOT_TOKEN in yml-file
docker-compose up -d

 
# bot.token
передать переменной при запуске кастомного контейнера BOT_TOKEN=
