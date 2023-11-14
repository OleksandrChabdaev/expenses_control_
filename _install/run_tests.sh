#!/usr/bin/env bash

cd ..
docker-compose down
#set -e
#docker-compose -f docker-compose-test.yml up -d --build --remove-orphans & docker-compose -f docker-compose-test.yml down -v
#docker-compose -f docker-compose-test.yml up -d --build
docker-compose -f docker-compose-test.yml down
docker-compose -f docker-compose-test.yml up -d pgdb
#sleep 5
#docker-compose -f docker-compose-test.yml run django ./manage.py test item.tests.ItemTestCase.test_create_item_by_owner
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test  aoi.tests.AOITestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test  aoi.tests.AOILimitedTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test  publisher.tests.ResultTestCase  --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test  aoi.tests.AOIResultRestrictedAclTestCase  --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test publisher.tests.BigGeojsonPublisherTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test publisher.tests.BigGeojsonWithStylePublisherTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test publisher.tests.GeotifPublisherTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test publisher.tests.PbdnnGeojsonPublisherTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test aoi.tests.JupyterNotebookTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test aoi.tests.RequestTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test aoi.tests.AOIRequestsTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test publisher.tests.WrongDatesTestCase --noinput
#docker-compose -f docker-compose-test.yml run webapplication ./manage.py test --noinput
#docker-compose -f docker-compose-test.yml exec webapplication ./manage.py test --keepdb
#docker-compose -f docker-compose-test.yml up -d --remove-orphans

#sleep 10
#set +e
docker-compose -f docker-compose-test.yml run django ./manage.py test
#STATUS=$?

#docker-compose -f docker-compose-test.yml down -v