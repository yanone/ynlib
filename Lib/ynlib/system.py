
def Execute(command):
	"""\
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
	"""\
	Calculate system power as integer using by mulitplying number of active CPUs with clock speed.
	"""
	from ynlib.system import Execute
	return int(Execute('sysctl hw.activecpu').split(' ')[-1]) * int(Execute('sysctl hw.cpufrequency').split(' ')[-1])

def MD5OfFile(filename):
	"""\
	Calculate hex MD5 sum of file.
	"""
	import hashlib
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
			 md5.update(chunk)
	return md5.hexdigest()






def GetChr(waitMaximalSeconds = None):
	"""\
	Wait for single keyboard press and return character
	"""

	import os
	import sys    
	import termios
	import fcntl
	import time

	firstCallTime = time.time()

	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
		while 1:
			try:
				c = sys.stdin.read(1)
				break
			except IOError: pass
			time.sleep(.1)
			
			# Return if waitMaximalSeconds is reached:
			if waitMaximalSeconds > 0:
				if time.time() > firstCallTime + waitMaximalSeconds:
					return None
			
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return c


def MachineName():
	import platform

	if platform.system() == 'Linux':
		
		cpu = ''
		itemsUsed = []
		procinfo = Execute('cat /proc/cpuinfo')

		for line in procinfo.split('\n'):
			if ':' in line:
				k, v = line.split(':')[:2]
				if k.strip() == 'model name' and not k in itemsUsed:
					cpu += v.strip()
					itemsUsed.append(k)
		return '%s %s with %s' % (Execute('cat /sys/devices/virtual/dmi/id/sys_vendor'), Execute('cat /sys/devices/virtual/dmi/id/product_name'), cpu)

	elif platform.system() == 'Darwin':

		name = None


		# Approach 1
		import sys
		import plistlib
		import subprocess
		from Cocoa import NSBundle
		data = plistlib.readPlistFromString(Execute('system_profiler -xml SPHardwareDataType'))

		if (len(sys.argv) == 2):
			model = sys.argv[1]
		else:
			model = subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.model"]).strip()

		serverInfoBundle=NSBundle.bundleWithPath_("/System/Library/PrivateFrameworks/ServerInformation.framework/")
		sysinfofile=serverInfoBundle.URLForResource_withExtension_subdirectory_("SIMachineAttributes", "plist", "")

		plist = plistlib.readPlist(sysinfofile.path())

		if (model in plist):
			name = plist[model]["_LOCALIZABLE_"]["marketingModel"]

		# Approach 2
		if not name:
			name = data[0]['_items'][0]['machine_name']


		return 'Apple %s (%s) with %s %s, %s memory' % (name, data[0]['_items'][0]['machine_model'], data[0]['_items'][0]['cpu_type'], data[0]['_items'][0]['current_processor_speed'], data[0]['_items'][0]['physical_memory'])

if __name__ == '__main__':
	print(MachineName())
	# print MachineName()[0]['_items']
	# print MachineName()[0]['_items'][0]['machine_name']
