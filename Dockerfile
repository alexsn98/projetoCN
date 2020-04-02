FROM ubuntu:18.04

#DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    apt install -y tzdata && \
    apt-get install -y python-pip python-dev && \
    apt install -y postgresql postgresql-contrib

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]