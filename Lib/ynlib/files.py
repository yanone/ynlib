def ReadFromFile(path):
	u"""\
	Return content of file
	"""
	import os, codecs
	if os.path.exists(path):
		f = codecs.open(path, encoding='utf-8', mode='r')
		text = f.read()
		f.close()
		return text

def WriteToFile(path, string):
	u"""\
	Write content to file
	"""
	f = open(path, 'w')
	f.write(string)
	f.close()
	return True