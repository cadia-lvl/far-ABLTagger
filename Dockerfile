FROM python:3.7

RUN mkdir /usr/src/app
COPY requirements.txt /usr/src/app/

RUN cd /usr/src/app \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

WORKDIR /usr/src/app
COPY . .

EXPOSE 8080

ENTRYPOINT uvicorn main:app --port 8080 --host 0.0.0.0
