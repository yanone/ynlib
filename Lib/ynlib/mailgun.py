# Import smtplib for the actual sending function
import os
import requests
import requests.auth

def mailgunemail(ACCESSPOINT, APIKEY, from_, to, subject, body, replyTo=None, cc=[], bcc=[], files=[]):

    assert type(from_) == str
    assert type(to) in (list, tuple)
    assert type(subject) == str
    assert type(body) == str
    assert type(cc) in (list, tuple)
    assert type(bcc) in (list, tuple)
    if replyTo:
        assert type(replyTo) == str

    url = "%s/messages" % ACCESSPOINT
    parameters = {
        "from": from_,
        "to": to,
        "subject": subject,
        "text": body,
    }

    if replyTo:
        parameters["h:Reply-To"] = replyTo
    if cc:
        parameters["cc"] = cc
    if bcc:
        parameters["bcc"] = bcc

    auth = ("api", APIKEY)
    if files:
        response = requests.post(
            url,
            data=parameters,
            auth=auth,
            # headers={'Content-type': 'multipart/form-data;'},
            files=files
            )
    else:
        response = requests.post(
            url,
            data=parameters,
            auth=auth,
            )
    if response.status_code != 200:
        return False, f"HTTP Error {response.status_code}, {response.text}"

    return True, None


class Email(object):
    """\
    Send email.
    recipients = ('post@example.com', 'another@example.com')
    """

    def __init__(self, ACCESSPOINT, APIKEY):
        self.recipients = []
        self.CC = []
        self.BCC = []
        self.sender = ''
        self.sendername = ''
        self.replyto = None
        self.subject = ''
        self.body = ''
        self.files = []
        self.APIKEY = APIKEY
        self.ACCESSPOINT = ACCESSPOINT

    def send(self):
        if self.sendername:
            sender = f"{self.sendername} <{self.sender}>"
        else:
            sender = self.sender
        return mailgunemail(
            self.ACCESSPOINT,
            self.APIKEY,
            sender,
            self.recipients,
            self.subject,
            self.body,
            replyTo=self.replyto,
            cc=self.CC,
            bcc=self.BCC,
            files=self.files)

    def attachFile(self, path=None, filename=None, binary=None):
        if path:
            filename = os.path.basename(path)
            self.files.append(("attachment", (filename, open(path, "rb").read())))
        elif binary and filename:
            self.files.append(("attachment", (filename, binary)))
        else:
            raise ValueError

if __name__ == "__main__":
    MAILGUNAPIKEY = ""
    MAILGUNACCESSPOINT = ""

    email = Email(MAILGUNACCESSPOINT, MAILGUNAPIKEY)
    email.subject = "Juicie Café: Trinkgeld"
    email.attachFile("mailgun.py")
    body = "Test"
    email.body = body
    email.recipients = ["post@yanone.de"]
    email.sender = "hq@juiciecafe.de"
    email.sendername = "Juicie Café HQ"
    print(email.send())
