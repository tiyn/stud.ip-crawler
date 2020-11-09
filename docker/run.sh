#!/bin/bash

while true; do python /studip/src/run.py -o /studip/src/data -u $USER -p $PSWD -s $URL --db_user $DB_USER --db_passwd $DB_PSWD --host $HOST && sleep $INTERVAL; done
