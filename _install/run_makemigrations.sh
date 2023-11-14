#!/usr/bin/env bash

cd ..
docker-compose down
docker-compose up  -d pgdb
sleep 10
#docker-compose run django ./manage.py makemigrations --empty user
#docker-compose run django ./manage.py makemigrations user
docker-compose run django ./manage.py migrate
#docker-compose run django ./manage.py createsuperuser
#docker-compose up -d