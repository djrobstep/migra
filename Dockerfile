FROM schemainspect

WORKDIR /migra
COPY . .

RUN poetry install && ln -s /migra/.venv/bin/migra /usr/local/bin/migra

CMD ["migra", "--help"]
