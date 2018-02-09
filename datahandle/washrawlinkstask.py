# coding:utf-8
import threading
from db import DB
class WashRawLinksTask(threading.Thread):
    
    def __init__(self, rooturl):
        super(WashRawLinksTask, self).__init__()
    
    def run(self):
        
        dbr = DB()
        
        pass
    
    @classmethod
    def dburlwashing(cls):
        pass