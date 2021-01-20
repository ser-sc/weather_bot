# weather_bot
Бот погоды для telegram
After setup
apt install python-pip
pip3 install pyTelegramBotAPI && pip3 install requests && pip3 install bs4
add line to crontab "*/1 * * * * python3 /home/ser/py_scr/weather_bot/bot.py"

Docker

docker build -t my-python-bot .
docker run -it --rm --name my-running-app my-python-bot
