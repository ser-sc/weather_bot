FROM python:alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt ./

# RUN был изменен, т.к. были проблемы с установкой psycopg2. В таком виде работает.
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY bot.py ./
COPY module.py ./
COPY dbconnect.py ./
COPY settings.py ./

CMD [ "python", "./bot.py" ]
