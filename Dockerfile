FROM python:3.6-alpine

COPY flask_query_api.py requirements.txt Querypkg /home/app/


RUN adduser -D -h /home/app app && pip3 install -r /home/app/requirements.txt

WORKDIR /home/app

USER app

ENTRYPOINT ["python3", "flask_query_api.py"]
