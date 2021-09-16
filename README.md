# weather_bot
Бот погоды для telegram
Для запуска необходимо *токен бота* передать переменной при запуске контейнера, либо вставить в Docker-compose

## Docker:

### сборка docker image:
docker build -t my-python-bot .

### создание и запуск docker container из docker image: 
docker run -d --restart=always --name my-bot --env BOT_TOKEN='*токен бота* без ковычек' my-python-bot


## Docker-compose:

### подготовка к запуску Docker-compose:
указать *токен бота* вместо <*токен бота* без ковычек> в yml-file

### сборка docker image, создание и запуск docker container из Docker-compose:
docker-compose up --build -d
