# -*- coding: utf-8 -*-


import datetime
from unidecode import unidecode
from ynlib.strings import smartString

def romanizeString(name):

	name = smartString(name)

	name = name.replace(smartString('ä'), smartString('ae'))
	name = name.replace(smartString('ö'), smartString('oe'))
	name = name.replace(smartString('ü'), smartString('ue'))
	name = name.replace(smartString('ß'), smartString('ss'))
	name = name.replace(smartString('Ä'), smartString('Ae'))
	name = name.replace(smartString('Ö'), smartString('Oe'))
	name = name.replace(smartString('Ü'), smartString('Ue'))

	name = unidecode(name)

	return name

class SEPATransfer(object):
	def __init__(self, accountHolder, BIC, IBAN, transferName):
		self.accountHolder = accountHolder
		self.BIC = BIC
		self.IBAN = IBAN
		self.transferName = transferName

		self.transactions = []

	def addTransaction(self, accountHolder, BIC, IBAN, transactionName, amount, subject):

		if IBAN != self.IBAN:
			transaction = SEPATransaction(accountHolder, BIC, IBAN, transactionName, amount, subject)
			self.transactions.append(transaction)

	def XML(self):

		xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.003.03" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:pain.001.003.03 pain.001.003.03.xsd">
	<CstmrCdtTrfInitn>
		<GrpHdr>
			<MsgId>''' + romanizeString(str(self.transferName)) + '''</MsgId>
			<CreDtTm>''' + datetime.datetime.now().isoformat() + '''</CreDtTm>
			<NbOfTxs>STILLEMPTY</NbOfTxs>
			<CtrlSum>STILLEMPTY</CtrlSum>
			<InitgPty>
				<Nm>''' + romanizeString(self.accountHolder) + '''</Nm>
			</InitgPty>
		</GrpHdr>
		<PmtInf>
			<PmtInfId>''' + romanizeString(str(self.transferName)) + '''</PmtInfId>
			<PmtMtd>TRF</PmtMtd>
			<BtchBookg>true</BtchBookg>
			<NbOfTxs>STILLEMPTY</NbOfTxs>
			<CtrlSum>STILLEMPTY</CtrlSum>
			<PmtTpInf>
				<SvcLvl>
					<Cd>SEPA</Cd>
				</SvcLvl>
			</PmtTpInf>
			<ReqdExctnDt>''' + datetime.date.today().isoformat() + '''</ReqdExctnDt>
			<Dbtr>
				<Nm>''' + romanizeString(self.accountHolder) + '''</Nm>
			</Dbtr>
			<DbtrAcct>
				<Id>
					<IBAN>''' + self.IBAN + '''</IBAN>
				</Id>
			</DbtrAcct>
			<DbtrAgt>
				<FinInstnId>
					<BIC>''' + self.BIC + '''</BIC>
				</FinInstnId>
			</DbtrAgt>
			<ChrgBr>SLEV</ChrgBr>
'''

		controlSum = 0
		for i, transaction in enumerate(self.transactions):
			xml += transaction.XML(i)
			controlSum += transaction.amount

		xml += '''\
		</PmtInf>
	</CstmrCdtTrfInitn>
</Document>
'''

		xml = xml.replace('<NbOfTxs>STILLEMPTY</NbOfTxs>', '<NbOfTxs>' + str(len(self.transactions)) + '</NbOfTxs>')
		xml = xml.replace('<CtrlSum>STILLEMPTY</CtrlSum>', '<CtrlSum>' + str(controlSum) + '</CtrlSum>')

		return xml

class SEPATransaction(object):

	def __init__(self, accountHolder, BIC, IBAN, transactionName, amount, subject):
		self.accountHolder = accountHolder
		self.BIC = BIC
		self.IBAN = IBAN
		self.transactionName = transactionName
		self.amount = float(amount)
		self.subject = subject

	def XML(self, i):


		xml = '''\
			<CdtTrfTxInf>
				<PmtId>
					<EndToEndId>''' + '%s-%s' % (romanizeString(self.transactionName), i) + '''</EndToEndId>
				</PmtId>
				<Amt>
					<InstdAmt Ccy="EUR">''' + str(self.amount) + '''</InstdAmt>
				</Amt>
				<CdtrAgt>
					<FinInstnId>
						<BIC>''' + str(self.BIC) + '''</BIC>
					</FinInstnId>
				</CdtrAgt>
				<Cdtr>
					<Nm>'''  + romanizeString(self.accountHolder) + '''</Nm>
				</Cdtr>
				<CdtrAcct>
					<Id>
						<IBAN>''' + str(self.IBAN) + '''</IBAN>
					</Id>
				</CdtrAcct>
				<RmtInf>
					<Ustrd>''' + romanizeString(self.subject) + '''</Ustrd>
				</RmtInf>
			</CdtTrfTxInf>
'''
		return xml


