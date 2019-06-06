#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import  sqlite3



class Database(object):

    def __init__(self, dbname):
        self.conn=sqlite3.connect(dbname, check_same_thread = False)
        self.sql={
            "create": """create table if not exists chat (
                                            id integer primary key, 
                                            from_name text not null,
                                            to_name text not null,
                                            message text) """,
            "insert": """insert into chat(from_name, to_name, message) values (?,?,?)""",
            "select": """select from_name, to_name, message from chat """

        }
        self.create()

    def create(self):
        cursor=self.conn.cursor()
        cursor.execute(self.sql["create"])
        cursor.close()

    def select(self, name=''):
        result=[]
        cursor=self.conn.cursor()
        if name == '':
            cursor.execute(self.sql["select"]+"where from_name=?", (name,))
        else:
            cursor.execute(self.sql["select"])
        result=cursor.fetchall()
        cursor.close()
        return result



    def insert(self, name_from, message, name_to=''):
        cursor=self.conn.cursor()
        if name_to=='':
            name_to='all'
        cursor.execute(self.sql["insert"],(name_from, name_to, message))
        self.conn.commit()
        cursor.close()



if __name__=="__main__":
    db=Database("test.db")
    db.insert(name_from="name1",name_to="name2",message="messgae")
    print(db.select())
