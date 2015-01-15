class EUInvoicing(object):
	def __init__(self, homeCountry, EUwithVATdict, clientCountry, clientVATID, netto):
		self.homeCountry = homeCountry
		self.EUwithVATdict = EUwithVATdict
		self.clientCountry = clientCountry
		self.clientVATID = clientVATID

		self.netto = netto
		self.tax = 0
		self.brutto = netto
		self.reverseCharge = False
		
		# DE
		if self.clientCountry == self.homeCountry:
			self.tax = self.netto * self.taxPercent(self.clientCountry)
			self.brutto = self.netto + self.tax

		# EU, private
		elif self.clientCountry in self.EUwithVATdict.keys() and not self.clientVATID:
			self.reverseCharge = True

		# EU, company
		elif self.clientCountry in self.EUwithVATdict.keys() and self.clientVATID:
			self.tax = self.netto * self.taxPercent(self.clientCountry)
			self.brutto = self.netto + self.tax

		# Outside EU
		else:
			pass
		

	def taxPercent(self, country):
		return int(self.EUwithVATdict[country]) / 100.0


EUwithVATdict = {
	'DE': 19,
	'FR': 20,
	'CZ': 21,
	}

i = EUInvoicing(
	homeCountry = 'DE',
	EUwithVATdict = EUwithVATdict,
	clientCountry = 'US',
	clientVATID = None,
	netto = 100.0
	)

print i.netto
print i.tax
print i.brutto
print i.reverseCharge