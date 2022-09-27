FROM postgres:13-alpine

ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV POSTGRES_USER=postgres
ARG LOCAL_USER

RUN printf "psql --username ${POSTGRES_USER} --command=\"CREATE USER ${LOCAL_USER} CREATEDB CREATEROLE;\"" > /docker-entrypoint-initdb.d/10-create-users.sh
RUN printf "psql --username ${POSTGRES_USER} --command=\"CREATE DATABASE ${LOCAL_USER};\"" > /docker-entrypoint-initdb.d/20-create-database.sh
