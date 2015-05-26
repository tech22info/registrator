#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import re,sys,string,shutil,subprocess
import random,os

# WeUse HTTPFOX

def GetConnection():
	cn_string=open(os.path.dirname(__file__)+'/.dbconnect.config','r')
	cns = cn_string.read()
	cn=psycopg2.connect(cns)
	cn_string.close()
	return cn

def translit(locallangstring):
    conversion = {
        u'\u0410' : 'A',    u'\u0430' : 'a',
        u'\u0411' : 'B',    u'\u0431' : 'b',
        u'\u0412' : 'V',    u'\u0432' : 'v',
        u'\u0413' : 'G',    u'\u0433' : 'g',
        u'\u0414' : 'D',    u'\u0434' : 'd',
        u'\u0415' : 'E',    u'\u0435' : 'e',
        u'\u0401' : 'Yo',   u'\u0451' : 'yo',
        u'\u0416' : 'Zh',   u'\u0436' : 'zh',
        u'\u0417' : 'Z',    u'\u0437' : 'z',
        u'\u0418' : 'I',    u'\u0438' : 'i',
        u'\u0419' : 'Y',    u'\u0439' : 'y',
        u'\u041a' : 'K',    u'\u043a' : 'k',
        u'\u041b' : 'L',    u'\u043b' : 'l',
        u'\u041c' : 'M',    u'\u043c' : 'm',
        u'\u041d' : 'N',    u'\u043d' : 'n',
        u'\u041e' : 'O',    u'\u043e' : 'o',
        u'\u041f' : 'P',    u'\u043f' : 'p',
        u'\u0420' : 'R',    u'\u0440' : 'r',
        u'\u0421' : 'S',    u'\u0441' : 's',
        u'\u0422' : 'T',    u'\u0442' : 't',
        u'\u0423' : 'U',    u'\u0443' : 'u',
        u'\u0424' : 'F',    u'\u0444' : 'f',
        u'\u0425' : 'H',    u'\u0445' : 'h',
        u'\u0426' : 'Ts',   u'\u0446' : 'ts',
        u'\u0427' : 'Ch',   u'\u0447' : 'ch',
        u'\u0428' : 'Sh',   u'\u0448' : 'sh',
        u'\u0429' : 'Sch',  u'\u0449' : 'sch',
        u'\u042a' : '"',    u'\u044a' : '"',
        u'\u042b' : 'Y',    u'\u044b' : 'y',
        u'\u042c' : '\'',   u'\u044c' : '\'',
        u'\u042d' : 'E',    u'\u044d' : 'e',
        u'\u042e' : 'Yu',   u'\u044e' : 'yu',
        u'\u042f' : 'Ya',   u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)

def get_random_birthday():
	day=random.choice(range(1,27))
	month=random.choice(range(1,12))
	year=2015-18-random.choice(range(1,25))
	return [day,month,year]

def get_random_name (male):
	cn=GetConnection()
	cr=cn.cursor()
	cr.execute('SELECT name FROM family_name WHERE male='+str(male)+' ORDER BY RANDOM() LIMIT 1;')
	family_name=cr.fetchone()[0]
	cr.execute('SELECT name FROM first_name WHERE male='+str(male)+' ORDER BY RANDOM() LIMIT 1;')
	first_name=cr.fetchone()[0]
	cr.execute('SELECT name FROM last_name WHERE male='+str(male)+' ORDER BY RANDOM() LIMIT 1;')
	last_name=cr.fetchone()[0]
	cr.close()
	cn.close()
	return [family_name,first_name,last_name]

def get_random_proxy():
	cn=GetConnection()
	cr=cn.cursor()
	cr.execute('SELECT ip_address, port FROM random_https_proxy;')
	pr_res=cr.fetchone()
	proxy=pr_res[0]
	port=str(pr_res[1])
	cr.close()
	cn.close()
	return [proxy,port]

