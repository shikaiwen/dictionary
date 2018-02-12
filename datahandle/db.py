# coding:utf-8
import sqlite3
import os
import json
import threading

class DB(object):
    
    lock = threading.Lock()
    
    def doFromZero(self):
        dbsql = """
            create table test(id int, name text)
        """
        conn = self.getconn()
        c = conn.cursor()
        c.execute(dbsql)
        conn.commit()
        c.close()
    
    def getconn(self):
        conn = sqlite3.connect(os.path.dirname(__file__) +"/worddb.db")
        return conn


    
    def exesql(self, sql):
        conn = self.getconn()
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        
    def exeSql(self, sql, data):
        with (DB.lock):
            conn = self.getconn()
            c = conn.cursor()
            c.execute(sql, data)
            
        
    def getrawwordbyversion(self,version,cnt):
        with (DB.lock):
            sql = "select * from jp_raw_word where version = ?"
            conn = self.getconn()
            c = conn.cursor()
            c.execute(sql, [version])
            dlist = c.fetchmany(cnt)
            return dlist
    
    
    def getwordtoquery(self):
        return self.getrawwordbyversion(0, 2)
        
        
    def saveRawTableData(self, listdata):
        with (DB.lock):
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
        with (DB.lock):
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

    def saveword(self, datalist):
        with (DB.lock):
            conn = self.getconn()
            c = conn.cursor()
            for t in datalist:
                param = [ t["word"], t["jm"], t["roma"], t["sd"],t["wordtype"], t["simpleDefinition"],json.dumps(t["sens"],ensure_ascii=False) ]
                c.execute("insert into hj_dict_data('word','jm','roma','sd','wordtype','simpleDefinition','sens') values(?,?,?,?,?,?,?)" , param)
            
            conn.commit()
            conn.close()
        
    def updatewordstatus(self, idlist, version):
        with (DB.lock):
            placeholder= '?' # For SQLite. See DBAPI paramstyle.
            placeholders = ', '.join(placeholder for unused in idlist)
            dbsql = 'update jp_raw_word set version = ? where id in (%s) ' % placeholders
                
            conn = self.getconn()
            c = conn.cursor()
            idlist.insert(0,version)
            c.execute(dbsql, idlist)
            
            conn.commit()
            conn.close()
        
    def rawlinks_save(self, datalist):
        with (DB.lock):
            conn = self.getconn()
            c = conn.cursor()
            
            mutival = [tuple([x]) for x in datalist]
            c.executemany("insert into raw_links(link) values (?)", mutival)
            
            conn.commit()
            conn.close()

