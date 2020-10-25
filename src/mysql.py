import time
import logging as log

import pymysql


class Database:

    def __init__(self, host, port, name, user, passwd, reset_dl):
        self.HOST = host
        self.PORT = port
        self.NAME = name
        self.USER = user
        self.PASSWD = passwd
        self.RESET_DL = reset_dl
        self.TABLE_FILE = 'files'
        self.setup_db()

    def connect(self):
        """
        Connect to an existing database instance based on the object attributes.
        """
        return pymysql.connect(
            host=self.HOST,
            port=self.PORT,
            user=self.USER,
            password=self.PASSWD,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def setup_db(self):
        """
        Creates a database with tables.
        """
        db = self.connect()
        crs = db.cursor()
        sql_query = "CREATE DATABASE IF NOT EXISTS " + self.NAME
        crs.execute(sql_query)
        db.select_db(self.NAME)
        query = "CREATE TABLE IF NOT EXISTS " + self.TABLE_FILE + \
            "(id CHAR(32) NOT NULL," + \
            "ch_date INT(11) NOT NULL," + \
            "PRIMARY KEY(id))"
        crs.execute(query)
        log.debug(db)

    def set_last_file_dl(self, file_id, time):
        """
        Insert a downloaded file to the database.

        Parameters:
        file_id (string): id of the file downloaded
        time(int): time the file was downloaded
        """
        db = self.connect()
        db.select_db(self.NAME)
        crs = db.cursor()
        log.debug('file: ' + file_id + ' time: ' + time)
        query = "INSERT INTO " + self.TABLE_FILE + "(`id`,`ch_date`)" + \
                "VALUES ('" + file_id + "','" + time + "')" + \
                "ON DUPLICATE KEY UPDATE `ch_date` = '" + time + "'"
        crs.execute(query)
        db.commit()

    def get_last_file_dl(self, file_id):
        """
        Check when a file was downloaded.

        Parameters:
        file_id(string): id of the file to check

        Returns:
        int: time when the file was downloaded last. None if it wasnt downloaded.
        """
        if self.RESET_DL:
            return None
        db = self.connect()
        db.select_db(self.NAME)
        crs = db.cursor()
        query = "SELECT ch_date FROM files WHERE id ='" + file_id + "'"
        crs.execute(query)
        res = crs.fetchone()
        if res != None:
            return res['ch_date']
        return None
