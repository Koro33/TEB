import json


class Singleton(object):
    '''
    Singleton baseclass
    '''
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Config(Singleton):
    '''
    Config using Singleton model
    '''
    def __init__(self):
        pass

    def conf_fromjson(self):
        '''
        read information from json files
        '''
        print('[INFO] try to Read TEB_config.json ...')
        try:
            with open("TEB_config.json", "r", encoding='utf-8') as f1:
                text = f1.read()
            TEB_configData = json.loads(text)
        except Exception:
            print(
                '[INFO] Read failed! Please check if the file [TEB_config.json] is existed...')
            exit()

        print('[INFO] Read succesful ...')

        return TEB_configData

    def TEB_getInfo(self, TEB_jsonData):

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

    def template_fromjson(self):
        '''
        read information from template
        '''
        print('[INFO] try to Read TEB_config.defualt.json ...')
        try:
            with open("TEB_config.defualt.json", "r", encoding='utf-8') as f1:
                text = f1.read()
            TEB_templateData = json.loads(text)
        except Exception:
            print(
                '[INFO] Read failed! Please check if the file [TEB_config.defualt.json] is existed...')
            exit()

        print('[INFO] Read succesful ...')

        return TEB_templateData


def main():
    c1 = Config()
    c2 = Config()
    c3 = Config().set()
    print(c1.set() == c2.set())
    print(c2.set() == c3)
    print(c1 is c2)
    print(id(c1), id(c2))
    print(c1._instance)


if __name__ == '__main__':
    main()
