#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import re,sys,string,shutil,subprocess
import random,os,web_api


def _reg_mailru_email(rproxy=web_api.get_random_proxy()):
	proxy=rproxy[0]
	port=rproxy[1]
	proxies = {
	"http": "http://"+proxy+":"+port,
	"https": "http://"+proxy+":"+port,
	}
	cn=web_api.GetConnection()
	cr=cn.cursor()
	registration_ok=False
	RPassword=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	UserMale=random.choice([True,False])
	if UserMale:
		Gen='1'
	else:
		Gen='2'
	UserFLF=web_api.get_random_name(UserMale)
	UserLogin=web_api.translit(UserFLF[0])+'.'+str(random.choice(range(1,10000)))
	RegDomain=random.choice(["mail.ru","bk.ru","inbox.ru","list.ru"])
	bd=web_api.get_random_birthday()
	try:
		page_=requests.get('https://m.mail.ru/cgi-bin/signup',proxies=proxies,timeout=60)
		page=page_.text
		x_reg_id=re.findall('name="x_reg_id" value="(.*?)"', page)[0]
		ID=re.findall('name="ID" value="(.*?)"', page)[0]
		Username=re.findall('type="text" id="Username" name="(.*?)"', page)[0]
	except:
		page='ERROR'
	try:
		ClassName=re.findall('<label for="(.*?)" class="name">Name', page)[0]
		Name=re.findall(' id="'+ClassName+'" name="(.*?)"', page)[0]
	except:
		ClassName=re.findall('<label for="(.*?)" class="name">Имя', page)[0]
		Name=re.findall(' id="'+ClassName+'" name="(.*?)"', page)[0]
	try:
		ClassLastName=re.findall('<label for="(.*?)" class="name">Last name<', page)[0]
		LastName=re.findall(' id="'+ClassLastName+'" name="(.*?)"', page)[0]
	except:
		ClassLastName=re.findall('<label for="(.*?)" class="name">Фамилия<', page)[0]
		LastName=re.findall(' id="'+ClassLastName+'" name="(.*?)"', page)[0]
	try:
		Gender=re.findall('"(.*?)" value="1">&nbsp;<span class="label">Male', page)[0].split('"')[-1]
	except:
		Gender=re.findall('"(.*?)" value="1">&nbsp;<span class="label">Мужской', page)[0].split('"')[-1]
	try:
		birthday=re.findall('class="birthday" name="(.*?)"', page)[0]
		birthyear=re.findall('class="birthyear" name="(.*?)"', page)[0]
		cookie=page_.cookies
		payload = {'MultistepMobileReg':'1','ID':ID,'Count':'1','back':'/cgi-bin/folders','browserData':'NoJS','lang':'','x_reg_id':x_reg_id,\
		Username:UserLogin,'RegistrationDomain':RegDomain,Name:UserFLF[1],LastName:UserFLF[0],Gender:Gen,birthday:str(bd[0]),'BirthMonth':str(bd[1]),birthyear:str(bd[2]),\
		'SavePost':'1','RegStep':'1','load':''}
	except:
		pass
	try:
		page_ = requests.post("https://m.mail.ru/cgi-bin/reg", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	except:
		page='ERROR'
		block_proxy_for_use(rp)
	# Stage_2
	page = page_.text
	Password=re.findall('id="password" autocomplete="off" maxlength="40" name="(.*?)"', page)[0]
	cookie=page_.cookies
	payload = {'MultistepMobileReg':'1','ID':ID,'Count':'1','back':'/cgi-bin/folders','browserData':'NoJS',\
	'lang':'','x_reg_id':x_reg_id,Password:RPassword,'RemindPhone':'','load':'','RegStep':'2'}
	try:
		page_ = requests.post("https://m.mail.ru/cgi-bin/reg", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	except:
		page='ERROR'
	cookie=page_.cookies
	page=page_.text
	captcha_link=re.findall('<p><img src="(.*?)" alt="" width="180" height="100"', page)[0]
	try:
		response = requests.get('https:'+captcha_link, stream=True,cookies=cookie,proxies=proxies,timeout=60)
	except:
		page='ERROR'
	with open('/tmp/img'+UserLogin+'.jpg', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	CaptchaID=re.findall('class="input-captcha" name="(.*?)"', page)[0]
	captcha=str(subprocess.check_output([os.path.dirname(__file__)+"/antigatepy2.py", "/tmp/img"+UserLogin+".jpg"]))
	captcha=captcha.split('\'')[1].split('\\')[0]
	os.remove("/tmp/img"+UserLogin+".jpg")
	payload = {'MultistepMobileReg':'1','ID':ID,'Count':'1','back':'/cgi-bin/folders','browserData':'NoJS','lang':'','x_reg_id':x_reg_id,\
	'RegStep':'10','security_image_id':'',CaptchaID:captcha}
	try:
		page_ = requests.post("https://m.mail.ru/cgi-bin/reg", data=payload ,cookies=cookie,proxies=proxies,timeout=60)
	except:
		page='ERROR'
	if page_.text.count('<meta http-equiv="refresh" content="0;url=https://m.mail.ru/cgi-bin/folders')>0:
		cr.execute('INSERT INTO email_mailru(email, domain, password, fio, birthday, male) VALUES (%s, %s, %s, %s, %s, %s);',(UserLogin,RegDomain,RPassword,\
		UserFLF[0]+' '+UserFLF[1]+' '+UserFLF[2],str(bd[0])+'.'+str(bd[1])+'.'+str(bd[2]),UserMale,))
		cn.commit()
		registration_ok=True
	else:
		pass
	cr.close()
	cn.close()
	return [registration_ok,UserLogin,RegDomain,RPassword]

def reg_mailru_email(rproxy=web_api.get_random_proxy()):
	try:
		result=_reg_mailru_email(rproxy)
	except:
		result=[False,'','','']
	return result