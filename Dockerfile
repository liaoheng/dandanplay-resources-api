FROM python:3.8-slim-buster

ARG MIRRORS="https://pypi.python.org/simple"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i $MIRRORS

ADD ddp_dmhy.py dmhy.py
ENTRYPOINT ["python","dmhy.py"]