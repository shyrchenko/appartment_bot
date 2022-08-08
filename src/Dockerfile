FROM python:3.8

RUN pip install --upgrade pip
RUN mkdir app
COPY /src/bot /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT python3 bot.py

