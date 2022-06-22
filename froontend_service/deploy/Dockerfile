FROM python:3.8-alpine

WORKDIR /server

RUN pip install --upgrade pip
COPY ./server/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./server/api.py ./app.py
COPY ./server/gunicorn.conf.py ./gunicorn.conf.py

COPY ./client/build ./build

EXPOSE 8080
CMD [ "gunicorn", "--log-level=debug", "app:app" ]
