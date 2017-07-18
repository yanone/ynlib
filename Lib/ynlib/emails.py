def SendEmail(recipients, sender, subject, body, attachments = None):

	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	msg = MIMEText(body)

	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ','.join(recipients)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(sender, recipients, msg.as_string())
	s.quit()




class Email(object):
	u"""\
	Send email.
	recipients = ('post@example.com', 'another@example.com')
	"""

	def __init__(self):
		self.recipients = []
		self.CC = []
		self.BCC = []
		self.sender = ''
		self.sendername = ''
		self.replyto = ''
		self.subject = ''
		self.body = ''
		self.attachments = []

	def send(self):
		
		# Import smtplib for the actual sending function
		import smtplib, os
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEBase import MIMEBase
		from email.MIMEText import MIMEText
		from email.Utils import COMMASPACE, formatdate
		from email import Encoders

		# Import the email modules we'll need
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		
		msg = MIMEMultipart()
		
		msg['MIME-Version']="1.0"
		msg['Content-Type'] = "text/plain;charset=utf-8"
		msg['Content-Transfer-Encoding'] = "quoted-printable"

		msg['Subject'] = self.subject
		msg['From'] = self.sender
		msg['To'] = ','.join(self.recipients)
		if self.CC:
			msg['Cc'] = ','.join(self.CC)
		msg.attach(MIMEText(self.body, 'plain', 'utf-8'))
		
		if self.replyto:
			msg.add_header('reply-to', self.replyto)

		for attachment in self.attachments:
			msg.attach(attachment.part)
		
		s = smtplib.SMTP('localhost')
		
		from sets import Set
		recipients = Set(self.recipients)
		recipients.update(Set(self.CC))
		recipients.update(Set(self.BCC))
		
		s.sendmail(self.sender, list(recipients), msg.as_string())
		s.quit()
		
		return list(recipients)

	def attachFile(self, path = None, filename = None, binary = None):
		self.attachments.append(EmailAttachment(path, filename))

class EmailAttachment(object):
	def __init__(self, path = None, filename = None, binary = None):
		self.path = path
		self.filename = filename
		self.binary = binary
	
		assert (self.path and os.path.exists(self.path)) or (self.filename and self.binary)

		self.part = MIMEBase('application', "octet-stream")

		if self.path:
			try:
				if os.path.exists(self.path):
					part.set_payload(open(self.path, "rb").read())
			except:
				part.set_payload(self.path)

		elif self.binary:
			part.set_payload(self.binary)

		Encoders.encode_base64(part)
		if self.filename:
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % self.filename)
		if self.path:
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(self.path))



	#%s %s' % (buy.localized('invoice'), os.path.basename(order.invoicePDFpath()))