
# coding:utf-8
import threading
from scrapper import Scrapper
from db import DB 
import time

class TaskUrlFetcher(threading.Thread):
    
    num = 1
    
    def __init__(self, rooturl):
        super(TaskUrlFetcher, self).__init__()
        self.rooturl = rooturl
    
    def run(self):
        
        scapper = Scrapper()
        linklist = scapper.loadLink(self.rooturl)
        
        dbr = DB()
        dbr.rawlinks_save(linklist)
        
        pass
    
    
    @classmethod
    def dburlwashing(cls):
        pass


if __name__ == '__main__':
    a = TaskUrlFetcher("")
    b = TaskUrlFetcher("")
    TaskUrlFetcher.num = 8
    a.num = 5
    print(str(a.num) + ":" + str(b.num) )
#     url = "https://qiita.com/konnyakmannan/items/2f0e3f00137db10f56a7#%E3%82%B5%E3%83%96%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%92%E4%BD%9C%E3%82%8B"
#     fetcher = UrlFetcherTask(url)
#     fetcher.start()
#     time.sleep(100000)