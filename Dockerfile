FROM alpine:3.8

RUN set -x && \
    apk add --no-cache bash python3 ca-certificates postgresql-libs postgresql-dev && \
    apk add --no-cache --virtual=build-dependencies build-base python3-dev && \
    pip3 install --upgrade --no-cache-dir pip && \
    pip3 install --no-cache-dir psycopg2-binary migra && \
    apk del build-dependencies postgresql-dev python3-dev && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

COPY docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["migra", "--help"]
