# coding:utf-8
import threading
import requests
import MeCab
from pyquery import PyQuery
from taskwashrawlinks import TaskWashRawLinks

class TaskFetchWord(threading.Thread):
    
    
    def __init__(self):
        
        pass
    
    def run(self):
        
        
        def nodefilter(i,node):
            return node.nodeType == 3
            
        
        while True:
            
            url = TaskWashRawLinks.getlink()
            resp = requests.get(url)
            if(resp.status_code == 200):
                text = resp.text
                t = MeCab.Tagger ("-Ochasen")
#                 print(text)
                d = PyQuery(text)
                d("html").find(":not(iframe)").contents().filter(nodefilter)
                m = t.parseToNode(text)
                wordlist = []
                while m:
#                     print(m.surface, "\t", m.feature)
                    fea = m.feature
                    word = fea.split(",")[-3]
                    if(word != "" and word != "*"):
                        wordlist.append(word)
                    m = m.next
                print(wordlist)
                break
        pass
    
if __name__ == "__main__":
    t = TaskFetchWord()
    t.run()
    pass