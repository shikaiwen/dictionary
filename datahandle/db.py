# coding:utf-8
import sqlite3
import os

class DB(object):
    
    def doFromZero(self):
        dbsql = """
            create table test(id int, name text)
        """
        conn = self.getconn()
        c = self.getcursor()
        c.execute(dbsql)
        conn.commit()
        c.close()
    
    def getconn(self):
        conn = sqlite3.connect(os.path.dirname(__file__) +"/worddb.db")
        return conn

    def getcursor(self):
        conn = self.getconn()
        c = conn.cursor()
        return c
    
    def exesql(self, sql):
        conn = self.getconn()
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        
    def saveRawTableData(self, listdata):
        dbsql = """
            insert into jp_raw_word values(NULL,?,?,?,?)
        """        
        conn = self.getconn()
        c = conn.cursor()
        
        for t in listdata:
            c.execute(dbsql , t)
        conn.commit()
        conn.close()
        
    def saveWordList(self, listdata):
#         // word(单词) jm(英文假名) roma(日语读音) sd(声调) fyf(说明内容，用换行符号分割)
        dbsql = """
            insert into jp_word(word,jm,roma,sd,fyf) values(?,?,?,?,?)
        """
        conn = self.getconn()
        c = conn.cursor()
        
        orderedlist = []
        for i in range(0,len(listdata)):
            dict = listdata[i]
            orderedlist.append((dict["word"], dict["jm"], dict["roma"], dict["sd"], dict["fyf"],dict["level"]  ))
        
        for t in orderedlist:
            c.execute("insert into jp_word('word','jm','roma','sd','fyf','level') values(?,?,?,?,?,?)" , t)
        conn.commit()
        conn.close()
        





    
