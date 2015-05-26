#!/usr/bin/python3
# encoding=utf-8
import sys
import web_api

proxy=web_api.get_random_proxy ()

print (proxy[0]+':'+proxy[1])