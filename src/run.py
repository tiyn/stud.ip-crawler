#!/bin/env python3
import os
import sys
import argparse
import logging as log

from studip import Studip
from crawler import Crawler
from mysql import Database


parser = argparse.ArgumentParser(description='Download Files from StudIP.')
parser.add_argument('-o', '--output', type=str,
                    default='./data', help='path to output directory')
parser.add_argument('-u', '--user', type=str,
                    help='studip username', required=True)
parser.add_argument('-p', '--passwd', type=str,
                    help='studip password', required=True)
parser.add_argument('-s', '--url', type=str, help='studip url', required=True)
parser.add_argument('--chunk', type=int, default=1024 *
                    1024, help='chunksize for downloading data')
parser.add_argument('-r', '--reset_dl_date', action='store_true',
                    help='downloads everything and ignores last download date')
parser.add_argument('--host', type=str, default='localhost', help='mysql host')
parser.add_argument('--port', type=int, default=3306, help='mysql port')
parser.add_argument('--db_name', type=str, default='studip',
                    help='mysql database name')
parser.add_argument('--db_user', type=str, default='root',
                    help='mysql database user')
parser.add_argument('--db_passwd', type=str,
                    default='secret-pw', help='mysql database password')
parser.add_argument('-d', '--debug_output', action='store_true',
                    help='display debug information about the process')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='only display most important output')
parser.add_argument('-l', '--log_file', action='store_true',
                    help='saves log to a log file named "log.txt"')
args = parser.parse_args()

if args.quiet:
    log_level = log.WARNING
elif args.debug_output:
    log_level = log.DEBUG
else:
    log_level = log.INFO

if args.log_file:
    log.basicConfig(level=log_level, filename='log.txt')
else:
    log.basicConfig(level=log_level)

BASE_DIR = os.path.abspath(args.output)
USERNAME = args.user
PASSWORD = args.passwd

db = Database(args.host, args.port, args.db_name,
              args.db_user, args.db_passwd, args.reset_dl_date)

studip = Studip(args.chunk, args.url, (USERNAME, PASSWORD), db)

crawler = Crawler(studip)

# Start crawling
try:
    crawler.download_curr_courses(BASE_DIR)
except KeyboardInterrupt:
    sys.exit(0)
