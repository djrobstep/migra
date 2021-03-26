FROM python:3.9-alpine

RUN apk add --update --no-cache --upgrade postgresql-libs && \
  apk add --no-cache --virtual=build-dependencies build-base postgresql-dev && \
  pip install --no-cache-dir packaging psycopg2-binary migra && \
  apk del build-dependencies && \
  rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

COPY docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["migra", "--help"]
