#!/bin/bash

while true; do python /studip/run.py -o /studip/data -u $USER -p $PSWD -s $URL --db_user $DB_USER --db_passwd $DB_PSWD --host $HOST && sleep $INTERVAL; done
