#!/usr/bin/python
#coding=utf-8

import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.163.com'
mail_user = 'xxxxx@163.com'
mail_pass = 'xxxxxxxxxxxxxxxxxxxxx'
#subject = 'test python'
#content = "This is a test Email"

def send_mail(mail_to_list, subject, content):
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = ";".join(mail_to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(mail_user, mail_to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
 