# -*- coding: utf-8 -*-

import smtplib

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def TEB_Info_to_mailsend_Info(TEB_Info):
    regular_info = []
    lowfee_info = []
    for room in TEB_Info:
        mailclient = TEB_Info[room]['mailclient']
        fee = TEB_Info[room]['Fee']
        alarm_threshold = TEB_Info[room]['alarm_threshold']

        regular_mailclient = [to_addr for [
            to_addr, isRegular] in mailclient.items() if isRegular]
        lowfee_mailclient = [to_addr for [to_addr, isRegular]
                             in mailclient.items() if not isRegular]

        for item in regular_mailclient:
            regular_info.append([item, room, fee])
        for item in lowfee_mailclient:
            if fee < alarm_threshold:
                lowfee_info.append([item, room, fee])

    return regular_info, lowfee_info


def mailSend(TEB_Info, admin_MailInfo):
    regular_info, lowfee_info = TEB_Info_to_mailsend_Info(TEB_Info)
    if regular_info:
        print('[INFO] Send mail to regular receiver: ' + ' \n')
        for regular_info_item in regular_info:
            regularMailSend(regular_info_item, admin_MailInfo)
    else:
        print('[INFO] No regular receiver!\n')

    if lowfee_info:
        print('[INFO] send mail to lowfee receiver' + ' \n')
        for lowfee_info_item in lowfee_info:
            lowfeeMailSend(lowfee_info_item, admin_MailInfo)
    else:
        print('[INFO] No lowfee receiver!\n')

    return


def regularMailSend(mailsend_Info, admin_MailInfo):
    '''

    '''
    from_addr = admin_MailInfo['mailserver_username']
    password = admin_MailInfo['mailserver_password']
    smtp_server = admin_MailInfo['mailserver_smtp']
    to_addr = mailsend_Info[0]
    # to_addr应该是被逗号分割的字符串，不能是list
    clientroom = mailsend_Info[1]
    fee = mailsend_Info[2]
    roominfo = clientroom.split('_')

    body = (" (つд⊂) \n"
            + " 嘉定" + " 校区  " + roominfo[1] + " 号楼  " + roominfo[2] + " 房间 \n"
            + " 电费还剩：" + str(fee))
    msg_from = ",".join(map(lambda from_addr: formataddr(
        (Header("勤奋的Robot", 'utf-8').encode(), from_addr)), [from_addr]))
    msg_to = ",".join(map(lambda to_addr: formataddr(
        (Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
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


def lowfeeMailSend(mailsend_Info, admin_MailInfo):

    from_addr = admin_MailInfo['mailserver_username']
    password = admin_MailInfo['mailserver_password']
    smtp_server = admin_MailInfo['mailserver_smtp']
    to_addr = mailsend_Info[0]
    # to_addr应该是被逗号分割的字符串，不能是list
    clientroom = mailsend_Info[1]
    fee = mailsend_Info[2]
    roominfo = clientroom.split('_')

    body = (" (つд⊂) \n"
            + " 嘉定" + " 校区  " + roominfo[1] + " 号楼  " + roominfo[2] + " 房间 \n"
            + " 电费还剩：" + str(fee))
    msg_from = ", ".join(map(lambda from_addr: formataddr(
        (Header("勤奋的Robot", 'utf-8').encode(), from_addr)), [from_addr]))
    msg_to = ", ".join(map(lambda to_addr: formataddr(
        (Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
    msg_subject = '[RPI_TEB]又没电了(╯°Д°)╯︵ ┻━┻'
    # msg_subject = '[RPI_TEB]电费报告...'

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
