# coding:utf-8
import threading
from db import DB
import time

# このthreadの機能は意味のないリンクを除きます

class TaskWashRawLinks(threading.Thread):
    
    def __init__(self):
        super(TaskWashRawLinks, self).__init__()
    
    @classmethod
    def getlink(self):
            db = DB()
            with(DB.lock):
                conn = db.getconn()
                cur = conn.cursor()
                cur.execute("select * from real_links where version=0")
                data = cur.fetchone()
                url = data[1]
                conn.commit()
                cur.close()
                return url
            return ""
    def run(self):
        
        
        while True:
            global db
            with(DB.lock):
                conn = db.getconn()
                cur = conn.cursor()
                cur.execute("select * from raw_links where id  = ( select min(id) from raw_links)")
                data = cur.fetchone()
                if(data is None):
                    pass
                else:
                    toinserturl = data[1]
                    cur.execute("select * from real_links where link  = ?", [toinserturl])
                    reallinkdata = cur.fetchone()
                    if(reallinkdata is None):
                        cur.execute("insert into real_links(link,version) values (?,?)", [toinserturl, 0])
    #                     もとのテーブルを削除する
                    cur.execute("delete from raw_links where link = ?", [toinserturl])
                conn.commit()
                cur.close()
            time.sleep(1)
                
    
    @classmethod
    def dburlwashing(cls):
        pass

if __name__ == '__main__':
    wa = TaskWashRawLinks()
    wa.run()