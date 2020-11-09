FROM python

LABEL maintainer "TiynGER <mail@martenkante.eu>"

ENV USER admin

ENV PSWD admin

ENV URL admin

ENV HOST mysql

ENV INTERVAL 86400

ENV DB_USER root

ENV DB_PSWD root

RUN git clone https://github.com/tiyn/stud.ip-crawler /studip

WORKDIR /studip

RUN pip install -r src/requirements.txt

ADD run.sh .

RUN chmod +x run.sh

RUN chmod +x src/run.py

VOLUME /studip/src/data

WORKDIR /studip/src

CMD ["/studip/run.sh"]
