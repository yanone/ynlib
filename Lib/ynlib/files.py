def ReadFromFile(path):
	"""\
	Return content of file
	"""
	import os, codecs
	if os.path.exists(path):
		f = codecs.open(path, encoding='utf-8', mode='r')
		text = f.read()#.decode('utf8')
		f.close()
		return text

	return ''

def WriteToFile(path, string):
	"""\
	Write content to file
	"""
	f = open(path, 'wb')
	f.write(string.encode())
	f.close()
	return True