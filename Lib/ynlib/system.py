def Execute(command):
	u"""\
	Execute system command, return output.
	"""

	import sys, os, platform

	if sys.version.startswith("2.3") or platform.system() == "Windows":

		p = os.popen(command, "r")
		response = p.read()
		p.close()
		return response


	else:

		import subprocess

		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
		os.waitpid(process.pid, 0)
		response = process.stdout.read().strip()
		process.stdout.close()
		return response

def Stamina():
	u"""\
	Calculate system power as integer using by mulitplying number of active CPUs with clock speed.
	"""
	from ynlib.system import Execute
	return int(Execute('sysctl hw.activecpu').split(' ')[-1]) * int(Execute('sysctl hw.cpufrequency').split(' ')[-1])

def MD5OfFile(filename):
	u"""\
	Calculate hex MD5 sum of file.
	"""
	import hashlib
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
			 md5.update(chunk)
	return md5.hexdigest()
