#!/bin/sh

while true; do python /studip/run.py -o /studip/data -u $USER -p $PSWD -s $URL && sleep $INTERVAL; done
