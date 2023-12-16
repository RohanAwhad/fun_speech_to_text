FROM python:3.11.6-slim-bullseye

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./main.py /app/main.py

EXPOSE 8000

CMD [ "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
