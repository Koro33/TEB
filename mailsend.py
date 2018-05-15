import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr


def _format_addr(s):
    '''
    邮件内容的重新编码
    '''
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def TEB_Info_to_mailsend_Info(TEB_Info):
    '''
    从 TEB_Info 中获取常态(regular)发送名单和低电费(lowfee)发送名单
    '''
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
    '''
    发送邮件，每一封都开服务单独发送
    (low method)
    '''
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
    常态邮件发送函数
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
    server.set_debuglevel(0)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()


def lowfeeMailSend(mailsend_Info, admin_MailInfo):
    '''
    低费用邮件发送函数
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
    msg_from = ", ".join(map(lambda from_addr: formataddr(
        (Header("勤奋的Robot", 'utf-8').encode(), from_addr)), [from_addr]))
    msg_to = ", ".join(map(lambda to_addr: formataddr(
        (Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
    msg_subject = '[RPI_TEB]又没电了(╯°Д°)╯︵ ┻━┻'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg['Subject'] = Header(msg_subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()


def adminMailSend(admin_MailInfo, admin_MailMsg):
    '''
    管理员管理邮件发送函数
    '''
    from_addr = admin_MailInfo['mailserver_username']
    password = admin_MailInfo['mailserver_password']
    smtp_server = admin_MailInfo['mailserver_smtp']
    to_addr = admin_MailInfo['admin_mailaddr']
    # to_addr应该是被逗号分割的字符串，不能是list

    body = ''
    for Msg in admin_MailMsg:
        body = body + Msg + '\n'

    msg_from = ",".join(map(lambda from_addr: formataddr(
        (Header("勤奋的Robot", 'utf-8').encode(), from_addr)), [from_addr]))
    msg_to = ",".join(map(lambda to_addr: formataddr(
        (Header("慵懒的管理员", 'utf-8').encode(), to_addr)), to_addr))
    msg_subject = '[RPI_TEB]电费报告(admin)...'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = msg_from
    msg['To'] = msg_to
    msg['Subject'] = Header(msg_subject, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    try:
        server.sendmail(from_addr, to_addr, msg.as_string())
    finally:
        server.quit()


class TEBmail(object):

    def __init__(self, **kwargs):
        self.smtp_server = None
        self.username = None
        self.password = None

        if kwargs.get('smtp_server'):
            self.smtp_server = kwargs['smtp_server']
        if kwargs.get('username'):
            self.username = kwargs['username']
        if kwargs.get('password'):
            self.password = kwargs['password']
        

    def show(self):
        print(self.smtp_server)
        print(self.username)
        print(self.password)

    def set_server(self, smtp_server, username, password):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password

    def test(self):
        from_name = '安徽省坚决反对'
        from_addr = ['ycg1024@qq.com', 'ycg1023@qq.com']
        # msg_from = formataddr([Header(from_name, 'utf-8').encode(), ', '.join(from_addr)])
        msg_from = ', '.join(
            map(lambda from_addr: formataddr([Header(from_name, 'utf-8').encode(), from_addr]), from_addr))
        print(msg_from)

    def mailsend(self, from_addr, to_addr, subject, content, from_name='', to_name=''):
        '''

        :param from_addr: list(only one element)
        :param to_addr: list
        :param subject: string
        :param content: string
        :return: None
        '''

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(
            [Header(from_name, 'utf-8').encode(), from_addr[0]])
        msg['To'] = ', '.join(map(lambda x: formataddr(
            [Header(to_name, 'utf-8').encode(), x]), to_addr))
        msg['Subject'] = Header(subject, 'utf-8').encode()

        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.username, self.password)
        try:
            server.sendmail(from_addr, to_addr, msg.as_string())
        except Exception:
            print("Can't send email!")
        finally:
            server.quit()

    def sendmail_admin(self):
        pass

    def sendmail_regular(self):
        pass

    def sendmail_lowfee(self):
        pass


def main():
    # m1 = TEBmail('smtp.sina.com', 'ycgdzq8j@sina.com', 'ycg135531')
    # m1.mailsend(['ycgdzq8j@sina.com'],['ycg1024@qq.com', '470413803@qq.com'],'test测试','testtesttest测试测试测试','测试测','测试是')
    # m1.test()

    # m1 = TEBmail(smtp_server='smtp.sina.com',username='ycgdzq8j@sina.com',password='ycg135531', iii='sdf')

    maill = {"username": "ycgdzq8j@sina.com",
             "password": "ycg135531",
             "smtp_server": "smtp.sina.com",
             "admin_mailaddr": "ycg1024@qq.com"}
    m1 = TEBmail(**maill)
    # m1.set_server('smtp.sina.com', 'ycgdzq8j@sina.com', 'ycg135531')
    m1.test()
    m1.show()


if __name__ == '__main__':
    main()
