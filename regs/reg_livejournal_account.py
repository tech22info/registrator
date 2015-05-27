#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import re,sys,string,shutil,subprocess
import random,os,web_api


def _Register_Livejournal_By_email (mail_id,rproxy=web_api.get_random_proxy()):
	proxy=rproxy[0]
	port=rproxy[1]
	proxies = {
	"http": "http://"+proxy+":"+port,
	"https": "http://"+proxy+":"+port,
	}
	cn=web_api.GetConnection()
	cr=cn.cursor()
	cr.execute('SELECT email, domain, password, fio, birthday, male FROM email_mailru WHERE id=%s;',(str(mail_id,)))
	email=cr.fetchone()
	result='[REGISTRATION ERROR]'
	try:
		cr.execute('INSERT INTO livejournal_accounts(email_id)  VALUES (%s);',(str(mail_id),))
		cn.commit()
	except:
		cn.rollback()
	cr.close()
	cn.close()
	# RegData prepare
	UserLogin=email[0].replace('.','').lower()
	UserLogin=''.join(UserLogin[1:5])+email[0].split('.')[1]
	Password=''.join(email[2][1:10])+''.join(email[0].upper()[1:10])+'12Yu'
	male='F'
	if email[5]:
		male='M'
	day=email[4].split('.')[0]
	mouth=email[4].split('.')[1]
	year=email[4].split('.')[2]
	page_=requests.get('https://www.livejournal.com/create?nojs=1',proxies=proxies,timeout=60)
	iframe='https://api-secure.solvemedia.com/'+re.findall('<iframe src="https://api-secure.solvemedia.com/(.*?)"', page_.text)[0]
	cookie=page_.cookies
	page_=requests.get(iframe,proxies=proxies,timeout=60)
	image=re.findall('<img src="(.*?)" alt="Typein Puzzle Challenge" id="adcopy-puzzle-image"', page_.text)[0]
	image='https://api-secure.solvemedia.com'+image
	response = requests.get(image, stream=True,cookies=cookie,proxies=proxies,timeout=60)
	cookie=page_.cookies
	with open('/tmp/_'+UserLogin+'.gif', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	page=page_.text
	k=re.findall('<input type=hidden name="k" value="(.*?)"', page)[0]
	l=re.findall('<input type=hidden name="l" value="(.*?)"', page)[0]
	t=re.findall('<input type=hidden name="t" value="(.*?)"', page)[0]
	s=re.findall('<input type=hidden name="s" value="(.*?)"', page)[0]
	magic=re.findall('<input type=hidden name="magic" value="(.*?)"', page)[0]
	adcopy_challenge=re.findall('<input type=hidden name="adcopy_challenge" id="adcopy_challenge" value="(.*?)"', page)[0]
	ref=re.findall('<input type=hidden name="ref" value="(.*?)"', page)[0]
	captcha=str(subprocess.check_output(["/opt/web_scripts/antigatepy2.py", '/tmp/_'+UserLogin+'.gif']))
	captcha=captcha.split('\'')[1].split('\\')[0]
	payload = {'adcopy_response':captcha,'k':k,'l':l,'t':t,'s':s,'magic':magic,'adcopy_challenge':adcopy_challenge}
	page_ = requests.post("https://api-secure.solvemedia.com/papi/verify.noscript", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	gilber_fish=re.findall('<META HTTP-EQUIV="REFRESH" CONTENT="0; URL=(.*?)"', page_.text)[0]
	page_ = requests.post(gilber_fish, data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	gilber_fish=re.findall('<textarea cols=30 rows=10 id=gibberish>(.*?)</textarea>', page_.text)[0]
	payload = {'username':UserLogin,'email':email[0]+'@'+email[1],'password':Password,'passwordconfirm':Password,'day':day,'month':mouth,'year':year,'gender':male,'adcopy_challenge':gilber_fish,'adcopy_response':'manual_challenge','create':'submit'}
	page_ = requests.post("https://www.livejournal.com/create?nojs=1", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	created=False
	if page_.text.count('Username is already in use')>1:
		result='[REGISTRED]'
	if page_.text.count(UserLogin)>5:
		result='[REGISTRATION OK]'
	return [result,Password,UserLogin]

def Register_Livejournal_By_email (mail_id,rproxy=web_api.get_random_proxy()):
	result=['[REGISTRATION ERROR]','','']
	try:
		result=_Register_Livejournal_By_email (mail_id,rproxy)
	except:
		pass
	cn=web_api.GetConnection()
	cr=cn.cursor()
	if result[0]=='[REGISTRED]' or result[0]=='[REGISTRATION OK]':
		cr.execute('UPDATE livejournal_accounts SET email_send=True, password=%s, login=%s WHERE email_id=%s;',(result[1],result[2],str(mail_id,)))
		cn.commit()
	else:
		cr.execute('UPDATE livejournal_accounts SET error_counter=error_counter+1 WHERE email_id=%s;',(str(mail_id,)))
		cn.commit()
	cr.close()
	cn.close()
	return result

def _Confirm_Livejournal_By_email (mail_id,rproxy=web_api.get_random_proxy()):
	result='[CONNECTION ERROR]'
	proxy=rproxy[0]
	port=rproxy[1]
	proxies = {
	"http": "http://"+proxy+":"+port,
	"https": "http://"+proxy+":"+port,
	}
	cn=web_api.GetConnection()
	cr=cn.cursor()
	cr.execute('SELECT email, domain, password, fio, birthday, male FROM email_mailru WHERE id=%s;',(str(mail_id,)))
	email=cr.fetchone()
	cr.execute('SELECT login, password FROM livejournal_accounts WHERE email_id=%s;',(str(mail_id,)))
	lg=cr.fetchone()
	payload = {'ret':'1','user':lg[0],'password':lg[1],'action:login':''}
	page_ = requests.post("https://www.livejournal.com/login.bml", data=payload ,proxies=proxies,timeout=60)
	cookie=page_.cookies
	page_=requests.get('http://'+lg[0]+'.livejournal.com/',proxies=proxies,cookies=cookie,timeout=60)
	if page_.text.count('<p class="js-controlstrip-status">You are viewing your journal</p>')>0:
		page_=requests.get('http://www.livejournal.com/',proxies=proxies,cookies=cookie,timeout=60)
		if page_.text.count('To gain access to all LiveJournal features you should validate your email.')>0:
			result='[ACCOUNT LOCKED]'
		else:
			result='[ACCOUNT CONFIRMED]'
	cr.close()
	cn.close()
	del page_
	if result!='[ACCOUNT CONFIRMED]':
		page_=requests.get('https://m.mail.ru/login',proxies=proxies,timeout=60)
		cookie=page_.cookies
		payload = {'post':'','mhost':'m.mail.ru','login_from':'','Login':email[0],'Domain':email[1],'Password':email[2]}
		page_ = requests.post("https://auth.mail.ru/cgi-bin/auth?rand=9763"+str(random.choice(range(1000,10000))), data=payload ,cookies=cookie,proxies=proxies,timeout=60)
		if page_.text.count('https://m.mail.ru/messages/inbox/')>0:
			cookie=page_.cookies
			page_=requests.get('https://m.mail.ru/messages/inbox/?back=1',proxies=proxies,cookies=cookie,timeout=60)
			page=page_.text
			Messages=re.findall('<a class="messageline__link" href="(.*?)"', page)
			for m_link in Messages:
				page_=requests.get('https://m.mail.ru'+m_link,proxies=proxies,cookies=cookie,timeout=60)
				page=page_.text
				From=re.findall('<span class="readmsg__addressed-word">(.*?)</strong></a>', page)[0]
				From=From.split('<strong>')[1]
				if From.count('do-not-reply@livejournal.com'):
					Confirm=re.findall('Please click on the following link to complete validation and set your primary email(.*?)</a>', page)[0]
					Confirm=Confirm.split('http://www.livejournal.<wbr>com')[1]
					confirm_url='http://www.livejournal.com'+Confirm.replace('<wbr>','')
					page_=requests.get('https://www.livejournal.com/login.bml',proxies=proxies,timeout=60)
					cookie_2=page_.cookies
					page=page_.text
					lj_form_auth=re.findall('name="lj_form_auth" value="(.*?)"', page)[0]
					payload = {'ret':'1','user':lg[0],'password':lg[1],'action:login':''}
					page_ = requests.post("https://www.livejournal.com/login.bml", data=payload ,proxies=proxies,cookies=cookie_2,timeout=60)
					cookie_2=page_.cookies
					page_=requests.get(confirm_url,proxies=proxies,cookies=cookie_2,timeout=60)
					if page_.text.count('Thanks!  The email address for')>0:
						result='[ACCOUNT CONFIRMED]'
	return result

def Confirm_Livejournal_By_email (mail_id,rproxy=web_api.get_random_proxy()):
	try:
		result=_Confirm_Livejournal_By_email (mail_id,rproxy)
	except:
		result='[CONNECTION ERROR]'
	if result=='[ACCOUNT CONFIRMED]':
		cn=web_api.GetConnection()
		cr=cn.cursor()
		cr.execute('UPDATE livejournal_accounts SET email_activated=True WHERE email_id=%s;',(str(mail_id),))
		cn.commit()
		cr.close()
		cn.close()
	return result

#print (Register_Livejournal_By_email (5,['127.0.0.1','3128']))
#print (Confirm_Livejournal_By_email (2,['127.0.0.1','3128']))
#print (Confirm_Livejournal_By_email (5))

