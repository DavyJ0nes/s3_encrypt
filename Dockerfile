FROM alpine:3.6
LABEL Name=s3_encrypt Version=0.0.1
LABEL Author=DavyJ0nes
LABEL Github=https://github.com/DavyJ0nes/s3_encrypt

RUN apk update && \
  apk add python3 && \
  ln -s /usr/bin/python3 /usr/bin/python && \
  ln -s /usr/bin/pip3 /usr/bin/pip && \
  mkdir -p /src/app

WORKDIR /src/app

ADD ./requirements /srv/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /src/app

CMD ["python"]
