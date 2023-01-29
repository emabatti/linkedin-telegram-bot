FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt install -y firefox-esr

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["python","app/main.py"]
