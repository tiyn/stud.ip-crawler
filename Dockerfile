FROM python

LABEL maintainer "TiynGER <mail@martenkante.eu>"

ENV USER admin

ENV PSWD admin

ENV URL admin

ENV HOST mysql

ENV INTERVAL 86400

ENV DB_USER root

ENV DB_PSWD root

ADD src /studip

WORKDIR /studip

RUN pip install -r requirements.txt

ADD docker-entry.sh .

RUN chmod +x docker-entry.sh

VOLUME /studip/data

WORKDIR /studip

CMD ["./docker-entry.sh"]
