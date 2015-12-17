# -*- coding: utf-8 -*-

from strings import *

def convertToEUR(source, amount = 1.0):
	u"""/
	
	"""
	from web import GetHTTP
	import json


	# STEP 1, confirm currency
	reply = json.loads(GetHTTP('http://www.apilayer.net/api/live?access_key=2c17819a3f130af5f5e867c77a362d27&currencies=%s' % source.upper()))
	if reply['success'] == True:


	
		url = 'http://www.apilayer.net/api/live?access_key=2c17819a3f130af5f5e867c77a362d27&currencies=EUR,%s' % source.upper()
	
		reply = json.loads(GetHTTP(url))
	
	
		base = reply['source']
	
		sourceValue = reply['quotes'][base + source.upper()]
		targetValue = reply['quotes'][base + 'EUR']
	
	
		return True, (float(targetValue / sourceValue) * float(amount))
	
	else:
		
		return False, reply['error']['info']

