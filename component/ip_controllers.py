from core.config import IP_CONFIG
import random
import time
import aiohttp
import json


class BaseController(object):
    def __init__(self):
        self.enable_ips = IP_CONFIG['ip_list']
        self.disable_ips = {}
        self.retry_interval = IP_CONFIG['ip_retry_interval']

    def get_ip(self):
        raise NotImplementedError("this method must override")

    def reuse_ip(self):
        raise NotImplementedError("this method must override")

class BinanceController(BaseController):
    def __init__(self, market_code, exception_handler):
        self.exception_handler = exception_handler
        self.market_code = market_code
        super(BinanceController, self).__init__()

    def get_ip(self):
        try:
            ip = random.choice(self.enable_ips)
        except IndexError:
            ip = None
        return ip

    def disable_ip(self, ip, timestamp):
        try:
            self.enable_ips.remove(ip)
        except KeyError:
            print("this ip dose not exist")
            return False

        self.disable_ips[ip] = timestamp
        return True

    def reuse_ip(self):
        for ip, timestamp in self.disable_ips.items():
            now_time = time.time()
            if now_time - timestamp >= self.retry_interval:
                result = self._test_ip(ip)
                if result is True:
                    self.enable_ips.append(ip)
                    del self.disable_ips[ip]
                else:
                    continue


    def _test_ip(self, ip):
        session = aiohttp.ClientSession()
        url = IP_CONFIG[self.market_code + '_test_url']
        response = session.get(url)
        data = json.loads(response.text)
        is_correct = self.exception_handler.is_correct(market_code=self.market_code, data=data)
        return is_correct
