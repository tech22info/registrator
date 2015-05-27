#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import re,sys,string,shutil,subprocess
import random,os,web_api

def _reg_fotostrana_account (email,domain,rproxy=web_api.get_random_proxy()):
	proxy=rproxy[0]
	port=rproxy[1]
	proxies = {
	"http": "http://"+proxy+":"+port,
	"https": "http://"+proxy+":"+port,
	}
	cn=web_api.GetConnection()
	cr=cn.cursor()
	cr.execute('SELECT id, email, domain, password, fio, birthday, male FROM email_mailru WHERE email=%s AND domain=%s;',(email,domain,))
	account=cr.fetchone()
	print (account)
	cr.close()
	cn.close()
	result='False'
	if account[6]:
		male='m'
	else:
		male='w'
	page_=requests.get('http://m.fotostrana.ru/signup/',proxies=proxies,timeout=60)
	page=page_.text
	ftoken=re.findall('id="ftoken-fSignup" name="ftoken-fSignup" value="(.*?)"', page)[0]
	csrftkn=re.findall('type="hidden" name="csrftkn" value="(.*?)"', page)[0]
	utk=re.findall('<input type="hidden" name="utk" value="(.*?)"', page)[0]
	#cookie=page_.cookies
	email=account[1]+'@'+account[2]
	print (email)
	payload = {'user_name':account[1],'user_email':email,'user_birthday_day':account[5].split('.')[0],'user_birthday_month':account[5].split('.')[1],'user_birthday_year':account[5].split('.')[2]\
	,'user_sex':male,'terms_agree':'on','ftoken-fSignup':ftoken,'csrftkn':csrftkn,'dudewhereismycar':'','submitted':'1','utk':utk}
	page_ = requests.post("http://m.fotostrana.ru/signup/signup", data=payload ,proxies=proxies,timeout=60)
	cookie=page_.cookies
	page=page_.text
	#print (ftoken+'  '+csrftkn+'  '+utk)
	captcha='/antispam/'+re.findall('<img alt="" src="/antispam/(.*?)"', page)[0]
	response = requests.get('http://m.fotostrana.ru'+captcha, stream=True,cookies=cookie,proxies=proxies,timeout=60)
	with open('/tmp/fs'+email+'.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	captcha=str(subprocess.check_output([os.path.dirname(__file__)+"/antigatepy2.py", "/tmp/fs"+email+".png"]))
	captcha=captcha.split('\'')[1].split('\\')[0]
	os.remove("/tmp/fs"+email+".png")
	#cookie=page_.cookies
	# Captcha
	# captcha_response_field=846077&ftoken-fSignup=f286bad9f0&csrftkn=c7227b7b9758b4b9717680c0e8f3cbeb&dudewhereismycar=&submitted=1&utk=509319
	ftoken=re.findall('id="ftoken-fSignup" name="ftoken-fSignup" value="(.*?)"', page)[0]
	csrftkn=re.findall('type="hidden" name="csrftkn" value="(.*?)"', page)[0]
	utk=re.findall('<input type="hidden" name="utk" value="(.*?)"', page)[0]
	payload = {'captcha_response_field':captcha,'ftoken-fSignup':ftoken,'csrftkn':csrftkn,'dudewhereismycar':'','submitted':'1','utk':utk}
	page_ = requests.post("http://m.fotostrana.ru/signup/signup", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	print (ftoken+'  '+csrftkn+'  '+utk)
	#print (page_.text)
	return result

print (_reg_fotostrana_account ('Krasichkova.6361','bk.ru',['127.0.0.1','3128']))
