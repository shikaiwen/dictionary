
# coding:utf-8



from _functools import reduce
from builtins import str
from lxml import etree
from openpyxl.xml.constants import MAX_ROW
from pyquery import PyQuery as pq
import json
import logging
import openpyxl
import openpyxl
import re
import requests
import sys
import unittest
import urllib
import sqlite3
import lxml
import os
from db import DB
# print(lxml.__file__)


try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True




proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Host":"dict.hjenglish.com",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

# requests.get('https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application')

# url = "https://dict.hjenglish.com/services/simpleExplain/jp_simpleExplain.ashx?type=jc&w=";
# resp.status_code == 200

def getquerywordlist():
    wb = openpyxl.load_workbook('C:/Users/shikw/Desktop/samples/jpword.xlsx')

    sheet1 = wb.get_sheet_by_name('Sheet1')
    sheet2 = wb.get_sheet_by_name('Sheet2')
     
    maxrow = sheet1.max_row
    maxcol = sheet1.max_column
    
    wordlist = []
    for r in range(1,maxrow):
        word = (sheet1.cell(row=r,column=1).value or "")
        if(word == ""): 
            continue
        else:
            wordlist.append(word)
    
    return wordlist

mm = [x  for x in getquerywordlist() if( x!="" and x.find("，")!=-1)]
print(mm)
exit()

def loadfromnet(wordlist):
    
    wordinfolist = []
    replaceArr = ["content","IfHasScb","hjd_langs","WordId","FromLang","ToLang"]
    for i in range(0,len(wordlist)-1):
        word = wordlist[i]
        resp = requests.post('https://dict.hjenglish.com/services/simpleExplain/jp_simpleExplain.ashx?type=jc&w='+word,headers= headers)
    
        if(resp.status_code != 200):
            sys.exit("http request 异常" +resp.request)
            return
        
        content = resp.text
        needed = content[content.find("{"): (content.rfind("}")+1) ]
        
        for c in range(0,len(replaceArr)):
            needed = needed.replace(replaceArr[c], "\"" + replaceArr[c] + "\"")
        dictjson = json.loads(needed)
        d = pq("<div>"+dictjson["content"] +"</div>")
        wordinfo = {}
        wordinfo["word"] = d("span.hjd_Green > font").html()
        wordinfo["roma"] = d("span:nth-child(2)").text()
        wordinfo["jm"] = d("span:nth-child(3)").text()
        wordinfo["sd"] = d("span:nth-child(4)").text()
        wordinfo["fyf"] = d("#hjd_wordcomment_1").attr("value")
        wordinfolist.append(wordinfo)
    return wordinfolist
    
db = DB()
# db.exesql("delete from jp_word")
wordlist = getquerywordlist()
loadedwordinfolist = loadfromnet(wordlist)
db.saveWordList(loadedwordinfolist)
# neededHtml = xhr.substr(content.indexOf("{"),content.lastIndexOf("}") - xhr.indexOf("{") +1)
#     
# 

