from ynlib.system import Execute

def GetHTTP(url, timeout = 5, authentication = None):
	u"""\
	GET HTTP responses from the net. Returns False if attempt failed.
	Authentication as "username:password"
	"""


	import urllib2, base64


	request = urllib2.Request(url)
	if authentication:
		base64string = base64.encodestring(authentication)
		request.add_header("Authorization", "Basic %s" % base64string)   
	result = urllib2.urlopen(request)




#	result = urllib2.urlopen(url, timeout = timeout)
#	request = urllib2.urlopen(url)
	if result.getcode() == 200:
		encoding = result.headers['content-type'].split('charset=')[-1]
		content = result.read()
		#print encoding
		try:
			content = unicode(content, encoding)
		except:
			pass
		return content
	else:
		return False
#	except:
#		return False

def PostHTTP(url, values = [], data = None, authentication = None, contentType = None):
	u"""\
	POST HTTP responses from the net. Values are dictionary {argument: value}
	Authentication as "username:password"
	"""

	import urllib, urllib2, base64
	
	if values:
		data = urllib.urlencode(values)
		
	headers = {}


	if contentType:
		headers["Content-Type"] = contentType
		headers["Accept"] = contentType

	if authentication:
#		base64string = base64.encodestring(authentication)
		headers["Authorization"] = "Basic %s" % Execute('printf %s | base64' % (authentication))

	request = urllib2.Request(url, data = data, headers = headers)
	response = urllib2.urlopen(request)
	return response.read()


def WhatsMyIP():
	u"""Pull your network's public IP address from the net, using whatsmyip.net"""

	import re
	whatsmyiphtml = GetHTTP("http://whatsmyip.net/")
	if whatsmyiphtml:
		m = re.search("""Your <acronym title="Internet Protocol">IP</acronym> Address is: <span>(.+?)</span>""", whatsmyiphtml)
		return m.group(1)
	else:
		return False
