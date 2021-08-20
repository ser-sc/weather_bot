FROM python:alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py ./
COPY module.py ./
COPY city.txt ./

CMD [ "python", "./bot.py" ]
