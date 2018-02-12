import smtplib
import time
import email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class GmailSmtpSender():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()

        self.server.login(username, password)

    def send_mail(self, destination, subject, content, signature=None):
        msg = MIMEMultipart('related') 
        msg['Subject'] = subject
        msg['To'] = destination
        msg['From'] = self.username
        
        msgText = MIMEText(_text=content)
        msg.attach(msgText)

        with open(signature, 'rb') as f:
            msgImage = MIMEImage(f.read())
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)

        self.server.send_message(msg)

