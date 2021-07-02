import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(email):
    msg = MIMEMultipart()
    msg['From'] = email.sender
    msg['To'] = email.recipient
    msg['Subject'] = email.subject

    msg.attach(MIMEText(email.message, 'plain'))

    if email.attachmentLocation != '':
        filename = os.path.basename(email.attachmentLocation)
        attachment = open(email.attachmentLocation, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email.sender, email.senderPw)
        text = msg.as_string()
        server.sendmail(email.sender, email.recipient, text)
        server.quit()
    except:
        raise Exception("SMPT server connection error - likely email credentials incorrect")
