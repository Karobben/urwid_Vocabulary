#!/usr/local/bin/python3.7
import argparse, sys

#命令行输入参数处理

####grep information from uniprot
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re, os, sys
import pandas as pd

import multiprocessing as mp
import time

WORD_DB = sys.path[0] +'/Needlman/DB_Word_Explain_WB'
print(sys.path[0])

def find_english(file):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    english = re.sub(pattern, '', file)
    return english

def Collins(Word):
    Result = ""
    url = "https://www.merriam-webster.com/dictionary/" + Word
    try:
        html = urlopen(url, timeout=10).read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        SOUP = soup.find_all("div",{"id":re.compile("dictionary-entry-")})
        Def = ""
        for i in SOUP:
            Def += i.get_text() + "\n\n"
        while "  " in Def:
            Def = Def.replace('  ',"\n\n")
        while "\n\n" in Def:
            Def = Def.replace('\n\n',"\n")
        Result = Def.strip()
    except:
        f = open("Fail.list",'a')
        f.write(Word+"\n")
        f.close()
    #print(Result)
    return Result

S_title = '''################
## Dictionary ##
################
'''
S0      = "\n################\n## Dictionary ##\n################\n"
S2      = "\n#######################\n## Synonyms & Origin ##\n#######################\n"
F_line  = "#"*5+"__DONE__"+"#"*5

def Trans(Word):
    Collins_W   = Collins(Word)
    if Collins_W != "":
        Result = S0+Word+"\t\n"*3+Collins_W+"\n\n"+Word+"\n"+F_line
        #print(Result)
        Add_DB(Result)
        return Result

def Add_DB(Result):
    File = open(WORD_DB,'a')
    File.write(Result+"\n")
    File.close()

def Refresh_DB():
    global DB
    File = open(WORD_DB,'r')
    DB_tmp = File.read().split(F_line)
    DB_tmp = list(set(DB_tmp))
    DB={}
    for i in DB_tmp:
        tmp=i.split("\t",1)
        try:
            DB.update({tmp[0].split('\n')[-1]:tmp[1]})
        except Exception as e:
            pass

def run_DB(word):
    try:
        print(DB[word],"YYYYYYY")
    except:
        try:
            Refresh_DB()
            print(DB[word])
        except:
            raise Error


CH1 = ''
CH2 = ''
CE  = ''
Word = "A"
DB = {}
Refresh_DB()

def Dic_WB(i):
    while "_" in i:
        i = i.replace("_",'')
    try:
        try:
            print(DB[i],CH1+F_linei+CE)
        except:
            Refresh_DB()
            print(DB[i],CH1+F_line+CE)
    except:
        Trans(i)
    Word = i
    return len(DB)
    #print(i, Word)

#print(Dic_WB('biolog#'))
