FROM python:3.6

WORKDIR /usr/src/app

COPY \
    requirements.txt \
    setup.py \
    README.md \
    ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "migra" ]
