# -*- coding: utf-8 -*-
import time
import asyncio

from core.config import LIMITER_CONFIG

monotonic = lambda : time.monotonic()
class BaseLimiter(object):
    def __init__(self, market_code):
        self.max_concurrent = LIMITER_CONFIG[market_code]["max_concurrent"]
        self.rate = LIMITER_CONFIG[market_code]['rate']
        self.market_code = market_code

    # 获取最大并发数
    def get_semaphore_concurrent(self):
        return self.max_concurrent

    # 对每个请求的时间进行限制
    def limit_per_request(self, symbol, response_time):
        raise NotImplementedError("this method must override")


class StandardLimiter(BaseLimiter):
    def __init__(self, *args, **kwargs):
        super(StandardLimiter, self).__init__(*args, **kwargs)

    def limit_per_request(self, symbol, response_time):
        try:
            limit_rate = LIMITER_CONFIG[self.market_code]['rate'][symbol]
        except KeyError:
            limit_rate = LIMITER_CONFIG[self.market_code]['rate']['default']

        # time.sleep(limit_rate)

class BinanceLimiter(BaseLimiter):
    def __init__(self, *args, **kwargs):
        super(BinanceLimiter, self).__init__(*args, **kwargs)

    def limit_per_request(self, symbol, response_time):
        try:
            limit_rate = LIMITER_CONFIG[self.market_code]['rate'][symbol]
        except KeyError:
            limit_rate = LIMITER_CONFIG[self.market_code]['rate']['default']

        time.sleep(limit_rate)