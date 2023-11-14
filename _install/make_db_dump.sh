#!/usr/bin/env bash
JSON_FILE=some_file.json

cd ../django_app
#docker-compose run webapplication python /code/manage.py dumpdata --indent 2 --output $JSON_FILE
#docker-compose run webapplication python /code/manage.py dumpdata > $JSON_FILE
#docker-compose -f ./docker-compose-stage.yml run django_stage python /code/manage.py loaddata $JSON_FILE
#docker-compose exec -T db pg_dump -U sip sip_db --data-only > dump_`date +%d-%m-%Y"_"%H_%M_%S`.dump
#docker-compose exec -T db pg_dump -U sip sip_db > db_`date +%d-%m-%Y"_"%H_%M_%S`.dump
docker exec -i pgdb /bin/bash -c "PGPASSWORD=x0zhuagn3 pg_dump --username expenses_control_user expenses_control" > db.dump