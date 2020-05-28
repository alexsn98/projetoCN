#!/bin/sh
export DEBIAN_FRONTEND=noninteractive

ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
apt-get install -y tzdata
dpkg-reconfigure --frontend noninteractive tzdata

apt update
yes | apt install postgresql postgresql-contrib
yes | apt install python3-pip
yes | pip3 install --upgrade pip
yes | pip3 install Flask
yes | pip3 install psycopg2-binary