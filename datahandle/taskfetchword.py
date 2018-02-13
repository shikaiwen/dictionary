#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import requests
import MeCab
from pyquery import PyQuery
from taskwashrawlinks import TaskWashRawLinks
import lxml.html
import lxml.etree
import unicodedata
import sys
import json
from db import DB

class TaskFetchWord(threading.Thread):
    
    
    def __init__(self):
        pass
    
    
    def parsenode(self, text):
        wordlist = []
        t = MeCab.Tagger (" ".join(sys.argv))
#         t = MeCab.Tagger ("-Ochasen")
        if(text.lstrip().rstrip() == ""):
            return wordlist
        m = t.parseToNode(text)
        while m:
            sur = m.surface
            fea = m.feature
            try:
                sur = m.surface
                fea = m.feature
                notwantword = [None, "*", ""]
                word = fea.split(",")[-3]
                if(word == "*" and sur not in notwantword): 
                    word = sur
                
                if(word not in notwantword):
                    wordlist.append(word)
            except BaseException as e:
                print(e)
            
#             if(fea.split(",")[-3] != "*"):
#                 word = fea.split(",")[-3]
#             
            m = m.next
        
        wordlist = list(filter(self.is_utf8str, wordlist))
        wordlist = list(filter(self.is_japanese, wordlist))
        
        return wordlist
    
    def run(self):
        
        
        while True:
            
        
            url = TaskWashRawLinks.getlink()
            resp = requests.get(url)
            
            if(resp.status_code != 200):
                continue
            
            allwordset = set([])
            text = resp.content
            d = PyQuery(text)
            for i,v in enumerate(d("html").find(":not(iframe)").contents()):
                text = ""
                if(isinstance(v,lxml.html.HtmlElement)):
                    text = PyQuery(v).text()
                elif(isinstance(v, lxml.etree._ElementUnicodeResult)):
                    text = str(v)
                if(text == ""):
                    continue
                
                wordlist = self.parsenode(text)
                if(len(wordlist)>0):
                    curjpset = set(wordlist)
                    allwordset |= curjpset
            
            TaskWashRawLinks.markprocessedlinkversion(url)            
#         return list(allwordset)
    
    
    def saverawwordtodb(self, wordlist):
        db = DB()
        with(DB.lock):
            conn = db.getconn()
            cur = conn.cursor()
            mutival = [tuple([x]) for x in wordlist]
            cur.execute("insert into real_links(word) values(?)", mutival)
            conn.commit()
            cur.close()
        return ""
    
    def is_utf8str(self, text):
        if( text in [None, "*", ""]):
            return True
        try:
            for c in text:
                c.encode("utf-8")
        except BaseException as e:
            return False
        return True
    def is_japanese(self, text):
#         print("is_japanese" + string)
        flag = True 
        for ch in text:
            try:
                name = unicodedata.name(ch) 
                if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
                    flag = True
                else:
                    return False
            except BaseException as e:
#                 print(e)
#                 print(text)
                flag = False
#                 pass

        return flag
    
    
if __name__ == "__main__":
    inst = TaskFetchWord()
    
    with(open("testfile.txt","a",encoding="utf-8")) as fd:
        s = json.dumps(list(inst.run()), ensure_ascii=False)
        print(s)
        fd.write(s)
        
        
#     print(inst.run())
#     sentence = "Pythonでマルチスレッド処理"
#     t = MeCab.Tagger (" ".join(sys.argv))
#     m = t.parseToNode(sentence)
#     wordlist = []
#     while m:
#         sur = m.surface
#         fea = m.feature
#         if(fea.split(",")[-3] != "*"):
#             wordlist.append(fea.split(",")[-3])
#         
#         if(fea.split(",")[-3] == "*" and inst.is_japanese(sur)):
#             wordlist.append(sur)
#         print(m.surface + "\t" + m.feature)
#         
#         m = m.next
    
#     print(wordlist)
    