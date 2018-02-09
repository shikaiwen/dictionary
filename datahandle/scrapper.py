# coding:utf-8
import requests
from pyquery import PyQuery
from urllib.parse import urlparse

class Scrapper:
    
    def loadLink(self, url):
        
        resp = requests.get(url)
        if(resp.status_code == 200):
            html = resp.text
            doc = PyQuery(html)
            linklist = []
            doc.find("a").each(lambda x,v: linklist.append(PyQuery(v).attr("href")))
            return self.wraptofullurl(url, linklist)
        return []
    
    
    def wraptofullurl(self,rooturl,urllist):
        o = urlparse(rooturl)
        addrurl = o.scheme + "://" + o.netloc
        resultlist = []
        
#         supportschemes = ["file"," ftp"," gopher"," hdl"," http"," https"," imap"," mailto"," mms"," news"," nntp"," prospero"," rsync"," rtsp"," rtspu"," sftp"," shttp"," sip"," sips"," snews"," svn"," svn+ssh"," telnet"," wais"," ws", "wss"]
        
        for i,elt in enumerate(urllist):
            if(([None, ""].count(elt) >0 ) or elt.startswith("#")):
                continue
            cur = urlparse(elt)
            wrappedurl = elt
            if( cur.scheme == ""):
                if(elt.startswith("/")):
                    wrappedurl = addrurl + elt
                else:
                    wrappedurl = addrurl + "/".join(o.path.split("/")[:-1]) + elt
            else:
                wrappedurl = elt
            resultlist.append(wrappedurl)    
            
        return resultlist