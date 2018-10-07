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

    def _throw_error_type(self, market_code, data):
        print(data)
        error_dict = DATA_ERROR_CONFIG[market_code]
        for key, value in error_dict.items():
            try:
                if data[key] == value[0]:
                    return value[1]
            except KeyError:
                continue
        return False


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
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        if except_type == "IP_BAN":
            timestamp = time.time()
        else:
            pass


class HuobiDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(HuobiDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if data["status"] == "ok":
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        if except_type == "INVALID_PARAMETER":
            spider_logger.warning("url parameter error")
        else:
            pass


class ZBDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(ZBDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "asks" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class ZBTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(ZBTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if isinstance(data, list):
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class HitBTCDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(HitBTCDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "asks" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class HitBTCTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(HitBTCTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "trades" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class OKEXDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(OKEXDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "asks" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class OKEXTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(OKEXTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if isinstance(data, list):
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class OKCoinDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(OKCoinDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "asks" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class OKCoinTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(OKCoinTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if isinstance(data, list):
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class PoloniexDepthExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(PoloniexDepthExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if "asks" in data:
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass


class PoloniexTradeExceptionHandler(BaseExceptionHandler):
    def __init__(self, *args, **kwargs):
        super(PoloniexTradeExceptionHandler, self).__init__(*args, **kwargs)

    def is_correct(self, market_code, data):
        if isinstance(data, list):
            return True
        else:
            except_type = self._throw_error_type(market_code, data)
            return except_type

    def handle_exception(self, spider_logger, except_type):
        pass
