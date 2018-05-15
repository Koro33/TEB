import json
import time

from selenium import webdriver  # 浏览器
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from Config import Config

inquiredict = dict(xiaoqu='嘉定校区', loudong='08号公寓',
                   louceng='三层', fangjian='301')





def TEB_getInfo(TEB_jsonData):

    TEB_Info = {}
    admin_MailMsg = []
    url = TEB_jsonData['target_url']
    headers = TEB_jsonData['headers']

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

def TEB_getInfo(TEB_jsonData):

    inquiredict = {}
    reg_maildict = {}
    low_maildict = {}
    subkey = ['username', 'password', 'smtp_server', 'admin_mailaddr']
    mailsever_info = {key: TEB_jsonData[key] for key in subkey}
    
    for key in TEB_jsonData['clientroom'].keys():
        inquiredict[key] = TEB_jsonData['clientroom'][key]['form_data']

        reg_addr = [addr for [addr, isRegular] in TEB_jsonData['clientroom'][key]['client_mailaddr'].items() if isRegular]
        reg_maildict[key] = {'maillist':reg_addr}
        
        low_addr = [addr for [addr, isRegular] in TEB_jsonData['clientroom'][key]['client_mailaddr'].items() if not isRegular]
        low_maildict[key] = {'maillist':low_addr,'alarm_threshold':TEB_jsonData['clientroom'][key]['alarm_threshold']}


    print(mailsever_info)
    print(inquiredict)
    print(reg_maildict)
    print(low_maildict)


inquiredict = {
    '1_8_301': {
        "xiaoqu": "嘉定校区",
        "loudong": "08号公寓",
        "louceng": "三层",
        "fangjian": "301"
    },
    '1_8_302': {
        "xiaoqu": "嘉定校区",
        "loudong": "08号公寓",
        "louceng": "三层",
        "fangjian": "302"
    },
    '1_8_303': {
        "xiaoqu": "嘉定校区",
        "loudong": "08号公寓",
        "louceng": "三层",
        "fangjian": "303"
    }
}


class TEB(object):
    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(25)

    def inquire(self, inquiredict):
        ''' '''
        balance_dict = {}
        for room, roominquiredict in inquiredict.items():
            try:
                self.browser.get('http://202.120.163.129:88/')
            except:
                print('TimeOut')
                self.browser.close()
                return None

            xiaoqu = self.browser.find_element_by_name("drlouming")
            select = Select(xiaoqu)
            select.select_by_visible_text(roominquiredict['xiaoqu'])

            loudong = self.browser.find_element_by_name("drceng")
            select = Select(loudong)
            select.select_by_visible_text(roominquiredict['loudong'])

            louceng = self.browser.find_element_by_name("dr_ceng")
            select = Select(louceng)
            select.select_by_visible_text(roominquiredict['louceng'])

            fangjian = self.browser.find_element_by_name("drfangjian")
            select = Select(fangjian)
            select.select_by_visible_text(roominquiredict['fangjian'])

            self.browser.find_element_by_id("usedR").click()

            try:
                self.browser.find_element_by_id("ImageButton1").click()
            except:
                print('TimeOut')
                self.browser.close()
                return None

            balance = self.browser.find_element_by_class_name("number").text
            balance_dict[room] = balance

        return balance_dict


def main():

    # teb1 = TEB()
    # balance_dict1 = teb1.inquire(inquiredict)
    # print(balance_dict1)
    cr = Config()
    cr.conf_fromjson()
    # TEB_jsonData = TEB_readfromjson()
    # print(TEB_jsonData)
    # print(inquiredict)
    # TEB_getInfo(TEB_jsonData)


if __name__ == '__main__':
    main()
