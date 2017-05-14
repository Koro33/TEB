# -*- coding: utf-8 -*-

import smtplib

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def regularMailSend(mailserver_username, mailserver_password, mailserver_smtp, mailclient, clientroom, fee):

    from_addr = mailserver_username
    password = mailserver_password
    smtp_server = mailserver_smtp
    to_addr = mailclient
    # to_addr应该是被逗号分割的字符串，不能是list

    body = (" (つд⊂) \n"
            + " 嘉定" + " 校区  " +
            str(clientroom)[-4] + " 号楼  " + str(clientroom)[-3:] + " 房间 \n"
            + " 电费还剩：" + str(fee))
    msg_from = ",".join(map(lambda from_addr: formataddr((Header("勤奋的Robot", 'utf-8').encode(), from_addr)), [from_addr]))
    msg_to = ",".join(map(lambda to_addr: formataddr((Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
    msg_subject = '[RPI_TEB]电费报告...'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg['Subject'] = Header(msg_subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()


def lowfeeMailSend(mailserver_username, mailserver_password, mailserver_smtp, mailclient, clientroom, fee):

    from_addr = [mailserver_username]
    password = mailserver_password
    smtp_server = mailserver_smtp
    to_addr = mailclient
    # to_addr应该是被逗号分割的字符串，不能是list

    body = (" (つд⊂) \n"
            + " 嘉定" + " 校区  " +
            str(clientroom)[-4] + " 号楼  " + str(clientroom)[-3:] + " 房间 \n"
            + " 电费还剩：" + str(fee))
    msg_from = ", ".join(map(lambda from_addr: formataddr(
        (Header("勤奋的Robot", 'utf-8').encode(), from_addr)), from_addr))
    msg_to = ", ".join(map(lambda to_addr: formataddr(
        (Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
    msg_subject = '[RPI_TEB]又没电了(╯°Д°)╯︵ ┻━┻'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg['Subject'] = Header(msg_subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()

'''
# %%
from email.header import Header
from email.utils import parseaddr, formataddr
mailclient = ["ycg1024@qq.com", "470413803@qq.com", "470413809@qq.com"]
#mailclient = ["ycg1024@qq.com"]
# mailclient = map(lambda x: "慵懒的管理员 <" + x + ">", mailclient)
to_addr = ", ".join(map(lambda addr: formataddr(
    (Header("慵懒的管理员", 'utf-8').encode(), addr)), mailclient))
print(to_addr)
'''