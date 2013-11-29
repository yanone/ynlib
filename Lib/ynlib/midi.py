import rtmidi, time

class MidiWithCallBack:
	def __init__(self):
		
		# SETUP MIDI
		self.midiin = rtmidi.RtMidiIn()
		
		self.functions = {}
		
		# Start listening
		self.midiin.setCallback(self.callFunction)

	def startListening(self):
		'''Start listenting'''
		self.midiin.openPort(0)
		while True:
			time.sleep(.1)
		self.midiin.closePort()

	def registerFunction(self, function, channel = None):
		'''Map function to MIDI channels'''
		
		if not channel:
			channel = -1
		
		self.functions[channel] = function

	def callFunction(self, midi):
		'''Call registered functions'''
		
		channel = midi.getControllerNumber()
		
		# Default mapping
		if not self.functions.has_key(channel):
			channel = -1

		# Call
		if self.functions.has_key(channel):
			f = self.functions[channel]
			#print f
			#eval(f.__name__ + '(midi)')
			f(midi)