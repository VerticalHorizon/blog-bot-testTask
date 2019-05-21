FROM python:3.7-alpine

WORKDIR /opt/application
COPY . /opt/application

RUN apk update && pip install -U pip && pip install pipenv && pipenv install --system --deploy

ENV PYTHONPATH=/opt/application

ENTRYPOINT ["python"]

CMD ["bot.py"]
