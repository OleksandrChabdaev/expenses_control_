#!/usr/bin/env bash

cd ..
docker-compose down
docker-compose up -d --build
#docker-compose up -d