#!/usr/bin/python
from antigate import AntiGate
import sys,os

apikeyfile=open(os.path.dirname(__file__)+'/.antigate.key','r')
apikey = apikeyfile.read()
apikeyfile.close()
gate = AntiGate(apikey, sys.argv[1])
print (gate)