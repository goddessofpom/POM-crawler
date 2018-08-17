from core.config import DATA_ERROR_CONFIG
import time
import traceback


class BaseExceptionHandler(object):
    def __init__(self,*args, **kwargs):
        pass

    def is_correct(self, market_code, data):
        raise NotImplementedError("this method must override")

    def handle_exception(self, spider_logger, except_type):
        raise NotImplementedError("this method must override")


class BinanceDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(BinanceDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        error_dict = DATA_ERROR_CONFIG[market_code]
        for key, value in error_dict.items():
            try:
                if data[key] == value[0]:
                    return value[1]
            except KeyError:
                continue
        return True

    def handle_exception(self, except_type, spider_logger, ip_controller=None, ip=None):
        if except_type == "IP_BAN" and ip_controller:
            spider_logger.warning("%s is banned" % ip)
            timestamp = time.time()
            ip_controller.disable_ip(ip, timestamp)


class BinanceTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(BinanceTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if isinstance(data, list):
            return True
        else:
            return False

    def handle_exception(self, spider_logger, except_type):
        spider_logger.error("error !!")
