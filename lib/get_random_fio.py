#!/usr/bin/python3
# encoding=utf-8
import sys
import web_api

male=True

try:
	if sys.argv[1]=='F':
		male=False
except:
	pass

print (web_api.get_random_name (male))