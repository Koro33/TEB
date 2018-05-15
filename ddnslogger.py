'''
logger defination
'''
import logging
import logging.handlers

class ddns_logger():
    ''' ddns_logger class '''
    def __init__(self, logger_name='DDNS_logger'):

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 创建一个轮转文件 Handler ，用于写入日志文件
        rfh = logging.handlers.RotatingFileHandler(
            'ddns.log', mode='a', maxBytes=204800, backupCount=1)
        rfh.setFormatter(formatter)

        self.logger.addHandler(rfh)

    def debug_msg(self, msg, *args, **kwargs):
        '''  '''
        self.logger.debug(msg, *args, **kwargs)

    def warning_msg(self, msg, *args, **kwargs):
        '''  '''
        self.logger.warning(msg, *args, **kwargs)

    def info_msg(self, msg, *args, **kwargs):
        '''  '''
        self.logger.info(msg, *args, **kwargs)

    def error_msg(self, msg, *args, **kwargs):
        '''  '''
        self.logger.error(msg, *args, **kwargs)

def test():
    dlog = ddns_logger()

    a = 123356

    dlog.debug_msg('This is debug message')
    dlog.info_msg('This is info message')
    dlog.warning_msg('This is warning message')
    dlog.error_msg('This is error message')

    dlog.info_msg('sdasf %s', a)

if __name__ == '__main__':
    test()