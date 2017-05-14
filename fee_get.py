# -*- coding: utf-8 -*-

import json
import requests
import lxml.html
from mailsend import *


def main():

    url = "http://202.120.163.129:88/"

    fee_threshold = 1.0

    print('[INFO] read TEB_config.json ...')
    with open("TEB_config.json", "r") as f:
        text = f.read()
    json_data = json.loads(text)
    print('[INFO] read succesful ...')

    headers = {'User-Agent': json_data['user_agent']}

    mailserver_username = json_data['mailserver_username']  # 发送提醒邮件的邮箱
    mailserver_password = json_data['mailserver_password']  # 发送提醒邮件邮箱的密码
    mailserver_smtp = json_data['mailserver_smtp']  # 发送邮箱的SMPT服务器地址

    for room in json_data['clientroom']:
        form_data = json_data['clientroom'][room]['form_data']
        mailclient = json_data['clientroom'][room]['mailclient']

        r = requests.post(url, headers=headers, data=form_data)
        page = lxml.html.document_fromstring(r.text)
        fee = float(page.xpath("//span[@class='number orange']/text()")[0])

        print(" 嘉定" + " 校区  " + str(room)[-4]
              + " 号楼  " + str(room)[-3:] + " 房间 " + " 电费还剩：" + str(fee))

        regular_mailclient = [to_addr for [to_addr, isRegular] in mailclient.items() if isRegular]

        if  regular_mailclient:
            print('[INFO] Send mail to regular receiver: ' + str(regular_mailclient))

            regularMailSend(mailserver_username=mailserver_username,
                            mailserver_password=mailserver_password,
                            mailserver_smtp=mailserver_smtp,
                            mailclient=regular_mailclient,
                            clientroom=room,
                            fee=fee)

        else:
            print('[INFO] No regular receiver!')

        lowfee_mailclient = [to_addr for [to_addr, isRegular] in mailclient.items() if not isRegular]

        if lowfee_mailclient:
            
            if fee < fee_threshold:
                print('[INFO] send mail to lowfee receiver' + str(lowfee_mailclient))
                lowfeeMailSend(mailserver_username=mailserver_username,
                               mailserver_password=mailserver_password,
                               mailserver_smtp=mailserver_smtp,
                               mailclient=lowfee_mailclient,
                               clientroom=room,
                               fee=fee)
        else:
            print('[INFO] No lowfee receiver!')

if __name__ == '__main__':
    main()
