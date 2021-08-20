# weather_bot
Бот погоды для telegram
Для запуска необходимо в корне репозитория создать файл bot.token с token бота:
 touch bot.token && echo "Ваш токен" >> bot.token


Docker:
docker build -t my-python-bot .
docker run -d --rm --name my-running-app my-python-bot
docker run --restart=always -d my-python-bot

 
# bot.token
Для создания бота и\или получения токена смотри инструкцию https://sendpulse.com/ru/knowledge-base/chatbot/create-telegram-chatbot
