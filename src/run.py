#!/bin/env python3
import os
import argparse

import studip
import mysql


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
parser.add_argument('-r', '--reset_dl_date', action='store_true', help='downloads everything and ignores last download date')
parser.add_argument('--host', type=str, default='localhost', help='mysql host')
parser.add_argument('--port', type=int, default=3306, help='mysql port')
parser.add_argument('--db_name', type=str, default='studip', help='mysql database name')
parser.add_argument('--db_user', type=str, default='root', help='mysql database user')
parser.add_argument('--db_passwd', type=str, default='secret-pw', help='mysql database password')
args = parser.parse_args()

BASE_DIR = os.path.abspath(args.output)
USERNAME = args.user
PASSWORD = args.passwd

db = mysql.Database()

db.HOST = args.host
db.PORT = args.port
db.DB_NAME = args.db_name
db.USER = args.db_user
db.PASSW = args.db_passwd
db.RESET_DL_DATE = args.reset_dl_date
db.setup_db()

crwlr = studip.Crawler(db)

crwlr.CHUNK_SIZE = args.chunk
crwlr.STUDIP_DOMAIN = args.url
crwlr.USER = (USERNAME, PASSWORD)

crwlr.download_curr_courses(BASE_DIR)
