FROM alpine:3.7

RUN apk add --no-cache python3 ca-certificates postgresql-dev && \
    apk add --no-cache --virtual=build-dependencies build-base python3-dev && \
    pip3 install --upgrade --no-cache-dir pip && \
    pip3 install --no-cache-dir psycopg2-binary migra && \
    apk del build-dependencies && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

ENTRYPOINT [ "/usr/bin/migra" ]

CMD ["--help"]

