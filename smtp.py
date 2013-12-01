#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, datetime

def TEXT(s):
	return s.decode('utf-8')

HOST     = 'smtp.qq.com'
# filepath = 'archive.zip'

def SendEmail(user, pwd, to, title, content, filepath = None):
	user     = user
	pwd      = pwd
	to       = to
	filepath = filepath
	title    = title
	content  = content
	msg = MIMEMultipart(content)
	if filepath != None and filepath != []:
		for path in filepath:
			att = MIMEText(open(path, 'rb').read(), 'base64', 'gb2312')
			att["Content-Type"] = 'application/octet-stream'
			att["Content-Disposition"] = 'attachment; filename="' + os.path.basename(path) + '"'
			msg.attach(att)
	part1 = MIMEText(content, 'plain')
	msg.attach(part1)

	msg['to'] = to
	msg['from'] = user
	msg['subject'] = Header(title, 'gb2312')
	msg.preamble = 'Our family reunion'

	server = smtplib.SMTP(HOST)
	server.login(user,pwd)
	error = server.sendmail(msg['from'], msg['to'], msg.as_string())
	server.close()
	if error:
		return (error)
	else:
		print 'success!'
		return 'send success!'

if __name__ == '__main__':
	send()