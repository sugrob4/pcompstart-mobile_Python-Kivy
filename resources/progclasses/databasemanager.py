# -*- coding: utf-8 -*-

import sqlite3


class DataBaseMnager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def querymany(self, *args):
        self.cur.executemany(*args)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.cur.close()
        self.conn.close()
