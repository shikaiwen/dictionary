#!/usr/bin/python
# -*- coding: utf-8 -*-

import MeCab
import sys
import string
import unicodedata
# 安装步骤
# 1 Mecab地址，安装时选择utf8，http://taku910.github.io/mecab/#install-windows
# 2 太坑了，官方没有说明windows版本的安装方式，自己用 pip search mecab, 搜索，找到windows版本安装

# C:\Program Files (x86)\MeCab\bin
def is_japanese( string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

# sentence = "太郎はこの本を二郎を見た女性に渡した。"
sentence = "homebrewのインストールしている，すべてのbrewをアンインストールする"
sentence = "Pythonでマルチスレッド処理"
try:

    print(MeCab.VERSION)

    t = MeCab.Tagger (" ".join(sys.argv))

    print(t.parse(sentence))
    m = t.parseToNode(sentence)
    wordlist = []
    while m:
        sur = m.surface
        fea = m.feature
        print(sur, "\t", fea)
        if(fea.split(",")[-3] == "*" and is_japanese(sur)):
            wordlist.append(sur)
        m = m.next
        
#         print("EOS")
    
    exit(0)
    lattice = MeCab.Lattice()
    t.parse(lattice)
    lattice.set_sentence(sentence)
    len = lattice.size()
    for i in range(len + 1):
        b = lattice.begin_nodes(i)
        e = lattice.end_nodes(i)
        while b:
            print("B[%d] %s\t%s" % (i, b.surface, b.feature))
            b = b.bnext 
        while e:
            print("E[%d] %s\t%s" % (i, e.surface, e.feature))
            e = e.bnext 
    print("EOS");

    d = t.dictionary_info()
    while d:
        print("filename: %s" % d.filename)
        print("charset: %s" %  d.charset)
        print("size: %d" %  d.size)
        print("type: %d" %  d.type)
        print("lsize: %d" %  d.lsize)
        print("rsize: %d" %  d.rsize)
        print("version: %d" %  d.version)
        d = d.next

except RuntimeError as e:
    print("RuntimeError:", e);