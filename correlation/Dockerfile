FROM ubuntu:18.04

RUN apt-get update -y && \
    ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    apt install -y tzdata && \
    apt-get install -y python-pip python-dev && \
    apt install -y postgresql postgresql-contrib

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "-b 0.0.0.0:5000"]