import time
import logging as log
import os

import sqlite3


class Database:

    def __init__(self, reset_dl):
        self.RESET_DL = reset_dl
        self.TABLE_FILE = 'files'
        self.DB_DIR = os.path.dirname(os.path.realpath(__file__))
        self.setup_db()

    def connect(self):
        """Connect to an existing database instance based on the object
        attributes.
        """
        path = os.path.join(self.DB_DIR, "data.db")
        return sqlite3.connect(path)

    def setup_db(self):
        """Creates a database with tables."""
        log.info("check database")
        db = self.connect()
        crs = db.cursor()
        query = "CREATE TABLE IF NOT EXISTS " + self.TABLE_FILE + \
            "(id CHAR(32) NOT NULL," + \
            "ch_date INT(11) NOT NULL," + \
            "PRIMARY KEY(id))"
        crs.execute(query)
        log.debug(db)

    def set_last_file_dl(self, file_id, time):
        """Insert a downloaded file to the database.

        Parameters:
        file_id (string): id of the file downloaded
        time(int): time the file was downloaded
        """
        db = self.connect()
        crs = db.cursor()
        log.debug('file: ' + file_id + ' time: ' + time)
        query = "INSERT INTO " + self.TABLE_FILE + "(`id`,`ch_date`)" + \
                "VALUES ( ?, ? )" + \
                "ON CONFLICT(`id`) DO UPDATE SET `ch_date` = ?"
        crs.execute(query, (file_id, time, time))
        db.commit()

    def get_last_file_dl(self, file_id):
        """Check when a file was downloaded.

        Parameters:
        file_id(string): id of the file to check

        Returns:
        int: time when the file was downloaded last. None if it wasnt downloaded.
        """
        if self.RESET_DL:
            return None
        db = self.connect()
        crs = db.cursor()
        query = "SELECT ch_date FROM files WHERE id = ?"
        crs.execute(query, (file_id, ))
        res = crs.fetchone()
        if res != None:
            return res[0]
        return None
