FROM alpine:latest

RUN apk add python3 py3-pip
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py /app.py
RUN chmod +x /app.py