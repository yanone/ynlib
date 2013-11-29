import plistlib, os

class Preferences(object):
	def __init__(self, appKey):
		self.appKey = appKey
		self.preferences = {}

		# plist
		self.plistfile = os.path.join(os.path.expanduser("~/Library/Preferences/"), self.appKey + '.plist')
		
		self.loadPreferences()
		
	def get(self, key):
		if self.preferences.has_key(key):
			return self.preferences[key]
		
	def set(self, key, value):
		self.preferences[key] = value
		self.savePreferences()
	
	def delete(self, key):
		if self.preferences.has_key(key):
			self.preferences.pop(key)
		self.savePreferences()

	def loadPreferences(self):
		if os.path.exists(self.plistfile):
			self.preferences = plistlib.readPlist(self.plistfile)
		
	def savePreferences(self):
		plistlib.writePlist(self.preferences, self.plistfile)
