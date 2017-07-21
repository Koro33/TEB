# -*- coding: utf-8 -*-

import json
import os
import time
import requests
import lxml.html
from mailsend import *


def TEB_readfromjson(mode=0):
    '''
    >>> read information from json files
    mode=0: RELEASE  
    mode=1: DEBUG
    '''
    if mode == 0:
        print('[INFO] try to Read TEB_config.json ...')
        try:
            with open("TEB_config.json", "r") as f1:
                text = f1.read()
            TEB_jsonData = json.loads(text)
        except Exception:
            print(
                '[INFO] Read failed! Please check if the file [TEB_config.json] is existed...')
            exit()
    else:
        print('[INFO] __DEBUG MODE__')
        print('[INFO] try to Read TEB_config_test.json ...')
        try:
            with open("TEB_config_test.json", "r") as f1:
                text = f1.read()
            TEB_jsonData = json.loads(text)
        except Exception:
            print(
                '[INFO] Read failed! Please check if the file [TEB_config_test.json] is existed...')
            exit()
    print('[INFO] Read succesful ...')

    return TEB_jsonData


def TEB_getFeeFromPage(url, headers, form_data):
    '''
    return (float)fee
    '''
    form_data_post = {
        "__VIEWSTATE": "",
        "__VIEWSTATEGENERATOR": "",
        "drlouming": "",
        "drceng": "",
        "dr_ceng": "",
        "drfangjian": "",
        "radio": "usedR",
        "ImageButton1.x": "",
        "ImageButton1.y": ""
    }
    # TEBsess = requests.session()
    with requests.Session() as TEBsess:

        r = TEBsess.get(url, headers=headers, timeout=5)  # 第1次 post
        page = lxml.html.document_fromstring(r.text)
        VIEWSTATE = page.xpath("//input[@name='__VIEWSTATE']/@value")
        VIEWSTATEGENERATOR = page.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value")
        form_data_post['__VIEWSTATE'] = VIEWSTATE
        form_data_post['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
        form_data_post['drlouming'] = form_data['drlouming']

        r = TEBsess.post(url, headers=headers,
                         data=form_data_post, timeout=5)  # 第2次 post
        page = lxml.html.document_fromstring(r.text)
        VIEWSTATE = page.xpath("//input[@name='__VIEWSTATE']/@value")
        VIEWSTATEGENERATOR = page.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value")
        form_data_post['__VIEWSTATE'] = VIEWSTATE
        form_data_post['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
        form_data_post['drceng'] = form_data['drceng']

        r = TEBsess.post(url, headers=headers,
                         data=form_data_post, timeout=5)  # 第3次 post
        page = lxml.html.document_fromstring(r.text)
        VIEWSTATE = page.xpath("//input[@name='__VIEWSTATE']/@value")
        VIEWSTATEGENERATOR = page.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value")
        form_data_post['__VIEWSTATE'] = VIEWSTATE
        form_data_post['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
        form_data_post['dr_ceng'] = form_data['dr_ceng']

        r = TEBsess.post(url, headers=headers,
                         data=form_data_post, timeout=5)  # 第4次 post
        page = lxml.html.document_fromstring(r.text)
        VIEWSTATE = page.xpath("//input[@name='__VIEWSTATE']/@value")
        VIEWSTATEGENERATOR = page.xpath(
            "//input[@name='__VIEWSTATEGENERATOR']/@value")
        form_data_post['__VIEWSTATE'] = VIEWSTATE
        form_data_post['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
        form_data_post['drfangjian'] = form_data['drfangjian']
        form_data_post['radio'] = form_data['radio']
        form_data_post['ImageButton1.x'] = form_data['ImageButton1.x']
        form_data_post['ImageButton1.y'] = form_data['ImageButton1.y']

        r = TEBsess.post(url, headers=headers,
                         data=form_data_post, timeout=5)  # 第5次 post
    page = lxml.html.document_fromstring(r.text)

    fee = float(page.xpath("//span[@class='number orange']/text()")[0])

    return fee


def TEB_getInfo(TEB_jsonData):
    '''
    return: 
    {'1_8_307': {
        'mailclient': {
            '******@qq.com': 0,
            '******@qq.com': 1
        },
        'Fee': 3.39
    }
    }
    '''
    TEB_Info = {}
    admin_MailMsg = []
    url = TEB_jsonData['target_url']
    headers = TEB_jsonData['headers']

    # mailserver_username = TEB_jsonData['mailserver_username']  # 发送提醒邮件的邮箱
    # mailserver_password = TEB_jsonData['mailserver_password']  # 发送提醒邮件邮箱的密码
    # mailserver_smtp = TEB_jsonData['mailserver_smtp']  # 发送邮箱的SMPT服务器地址
    # admin_mail = TEB_jsonData['admin_mailaddr']  # 管理员邮箱
    subkey = ['mailserver_username', 'mailserver_password',
              'mailserver_smtp', 'admin_mailaddr']
    admin_MailInfo = {key: TEB_jsonData[key] for key in subkey}

    for room in TEB_jsonData['clientroom']:
        alarm_threshold = TEB_jsonData['clientroom'][room]['alarm_threshold']
        form_data = TEB_jsonData['clientroom'][room]['form_data']
        mailclient = TEB_jsonData['clientroom'][room]['client_mailaddr']
        fee = TEB_getFeeFromPage(url, headers, form_data)
        TEB_Info[room] = {'Fee': fee, 'mailclient': mailclient,
                          'alarm_threshold': alarm_threshold}
        roominfo = room.split('_')

        msg = " 嘉定" + " 校区  " + \
            roominfo[1] + " 号楼  " + roominfo[2] + " 房间 " + " 电费还剩：" + str(fee)
        admin_MailMsg.append(msg)

    return TEB_Info, admin_MailInfo, admin_MailMsg


def TEB_Info_log():
    '''

    '''
    localtime = time.localtime()
    print(time.strftime('%Y-%m-%d %H:%M:%S', localtime))
    return


def send_adminmail(admin_MailInfo, admin_MailMsg):

    return


def main():
    '''

    '''
    TEB_jsonData = TEB_readfromjson(mode=0)  # 从json文件中读取条目
    TEB_Info,  admin_MailInfo, admin_MailMsg = TEB_getInfo(TEB_jsonData)

    print(TEB_Info)
    print(admin_MailInfo)
    print(admin_MailMsg)

    regular_info, lowfee_info = TEB_Info_to_mailsend_Info(TEB_Info)
    print(regular_info)
    print(lowfee_info)
    mailSend(TEB_Info, admin_MailInfo)


if __name__ == '__main__':
    main()
