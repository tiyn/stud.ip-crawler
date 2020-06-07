#!/bin/env python3
import time

import pymysql


class Database:

    def __init__(self):
        self.HOST = None
        self.PORT = None
        self.DB_NAME = None
        self.USER = None
        self.PASSW = None
        self.TABLE_FILE = None
        self.TABLE_FILE = 'files'
        self.RESET_DL_DATE = False

    def connect(self):
        return pymysql.connect(
            host=self.HOST,
            port=self.PORT,
            user=self.USER,
            password=self.PASSW,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def setup_db(self):
        db = self.connect()
        crs = db.cursor()
        sql_query = "CREATE DATABASE IF NOT EXISTS " + self.DB_NAME
        crs.execute(sql_query)
        db.select_db(self.DB_NAME)
        query = "CREATE TABLE IF NOT EXISTS " + self.TABLE_FILE + \
            "(id CHAR(32) NOT NULL," + \
            "ch_date INT(11) NOT NULL," + \
            "PRIMARY KEY(id))"
        crs.execute(query)
        print(db)

    def set_last_file_dl(self, file_id, time):
        db = self.connect()
        db.select_db(self.DB_NAME)
        crs = db.cursor()
        print('file: ', file_id, ' time: ', time)
        query = "INSERT INTO " + self.TABLE_FILE + "(`id`,`ch_date`)" + \
                "VALUES ('" + file_id + "','" + time + "')" + \
                "ON DUPLICATE KEY UPDATE `ch_date` = '" + time + "'"
        crs.execute(query)
        db.commit()

    def get_last_file_dl(self, file_id):
        if self.RESET_DL_DATE:
            return None
        db = self.connect()
        db.select_db(self.DB_NAME)
        crs = db.cursor()
        query = "SELECT ch_date FROM files WHERE id ='" + file_id + "'"
        crs.execute(query)
        res = crs.fetchone()
        if res != None:
            return res['ch_date']
        return None
