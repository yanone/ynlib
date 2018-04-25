# -*- coding: utf-8 -*-

def GetHTTP(url, timeout = 5, authentication = None):
	"""\
	GET HTTP responses from the net. Returns False if attempt failed.
	Authentication as "username:password"
	"""


	import urllib.request, urllib.error, urllib.parse, base64, certifi


	request = urllib.request.Request(url)
	if authentication:
		base64string = base64.encodestring(authentication)
		request.add_header("Authorization", "Basic %s" % base64string)   
	result = urllib.request.urlopen(request, cafile=certifi.where())





#	result = urllib2.urlopen(url, timeout = timeout)
#	request = urllib2.urlopen(url)
	if result.getcode() == 200:
		encoding = result.headers['content-type'].split('charset=')[-1]
		content = result.read()
		#print encoding
		try:
			content = str(content, encoding)
		except:
			pass
		return content
	else:
		return False
#	except:
#		return False

def PostHTTP(url, values = {}, data = None, authentication = None, contentType = None, files = []):
	"""\
	POST HTTP responses from the net. Values are dictionary {argument: value}
	Authentication as "username:password".
	Files as list of paths.
	"""

	import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, base64
	
	if values:
		data = urllib.parse.urlencode(values)
		
	headers = {}


	if contentType:
		headers["Content-Type"] = contentType
		headers["Accept"] = contentType

	if authentication:
		base64string = base64.encodestring(authentication)
		headers["Authorization"] = "Basic %s" % base64string

	request = urllib.request.Request(url, data = data, headers = headers)
	response = urllib.request.urlopen(request)
	return response.read()

def PostFiles(url, values):

	import urllib.request, urllib.error, urllib.parse

	import poster.encode
	import poster.streaminghttp

	opener = poster.streaminghttp.register_openers()

	datagen, headers = poster.encode.multipart_encode(values)
	response = opener.open(urllib.request.Request(url, datagen, headers))
	return response.read()

def WhatsMyIP():
	"""Pull your network's public IP address from the net, using whatsmyip.net"""

	import re
	whatsmyiphtml = GetHTTP("http://whatsmyip.net/")
	if whatsmyiphtml:
		m = re.search("""Your <acronym title="Internet Protocol">IP</acronym> Address is: <span>(.+?)</span>""", whatsmyiphtml)
		return m.group(1)
	else:
		return False

def FollowURL(url):
	import requests
	r = requests.get(url)
	return r.url

