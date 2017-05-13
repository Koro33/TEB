# -*- coding: utf-8 -*-

import smtplib
import json

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def mailsend(fare):

    print('read config.json ...')

    with open("config.json", "r") as f:
        text = f.read()
    json_data = json.loads(text)
    username = json_data['username'] # 发送提醒邮件的邮箱
    password = json_data['password'] # 发送提醒邮件邮箱的密码
    client = json_data['client'] # 接受提醒的邮箱
    server = json_data['server'] # 发送邮箱的SMPT服务器地址

    print('read successful ...')
    # print('username: ' + username + '\n' + 'password: ' + password + '\n' + 'client: '+ client + '\n' + 'server: '+ server+ '\n')

    from_addr = username
    password = password
    to_addr = client
    smtp_server = server

    body = "电费还剩：" + str(fare) + " (つд⊂) "

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = _format_addr('勤奋的Robot <%s>' % from_addr)
    msg['To'] = _format_addr('伟大的管理员 <%s>' % to_addr)
    msg['Subject'] = Header('又没电了...', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

