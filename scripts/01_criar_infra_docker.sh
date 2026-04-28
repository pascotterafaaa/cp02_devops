#!/usr/bin/env bash
set -e

docker pull mysql:8.0
docker pull adminer:latest

docker network create rede_564928
docker volume create vol_db_564928

docker run \
  --name db_564928 \
  -d \
  --network rede_564928 \
  -e MYSQL_ROOT_PASSWORD=senha_564928 \
  -e MYSQL_DATABASE=dimdim_564928 \
  -e MYSQL_USER=user_564928 \
  -e MYSQL_PASSWORD=senha_564928 \
  -p 3306:3306 \
  -v vol_db_564928:/var/lib/mysql \
  -v "$(pwd)/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql" \
  mysql:8.0

docker run \
  --name adminer_564928 \
  -d \
  --network rede_564928 \
  -e ADMINER_DEFAULT_SERVER=db_564928 \
  -p 8080:8080 \
  adminer:latest

docker ps
