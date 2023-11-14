#!/usr/bin/env bash

cd ..

#docker-compose run -u 1000:1000 react npx create-react-app .
#docker-compose run react yarn add axios dayjs jwt-decode react-router-dom@5.2.0
#docker-compose run react yarn add axios react-router-dom
#docker-compose run react yarn add bootstrap
#docker-compose run react yarn add prettier -D
#docker-compose run react yarn add reactjs-social-login
docker-compose run react yarn add @react-oauth/google
