#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import re,sys,string,shutil,subprocess
import random,os,web_api,check_mailru_email

# Измените данные на подключение к реальной базе данных
cn_string = "host='127.0.0.1' dbname='mailru_emails' user='web_script' password='web_script'"
cn=psycopg2.connect(cn_string)
cr=cn.cursor()
cr.execute('SELECT email, domain, password FROM emails WHERE status=\'[CONNECTION ERROR]\' ORDER BY Random() LIMIT 1;')
#cr.execute('SELECT email, domain, password FROM emails WHERE email=\'Apreutesey.3476\'')
email=cr.fetchone()
#print (email)
result=check_mailru_email.check_login_mailru(email[0],email[1],email[2])
#print (result)

cr.execute('UPDATE emails SET status=%s WHERE email=%s AND domain=%s;',(result,email[0],email[1],))
cn.commit()

cr.close()
cn.close()
