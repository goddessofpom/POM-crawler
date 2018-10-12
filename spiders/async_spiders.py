from celery_service.big_deals import save_big_deals
from core.base_spider import BaseSpider


class BinanceDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(BinanceDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        # redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        redis_key = "depth:" + market_code
        return redis_key

    def save(self, redis_key, data, symbol=None):
        # self.redis.hset(redis_key, "bids", data["bids"])
        # self.redis.hset(redis_key, "asks", data["asks"])
        self.redis.hset(redis_key, symbol, data)

    def broadcast_data(self, data):
        pass


class BinanceTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(BinanceTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        # redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        redis_key = "trade:" + market_code
        return redis_key

    def save(self, redis_key, data, symbol=None):
        # self.redis.ltrim(redis_key, 1, 0)
        # self.redis.rpush(redis_key, *data)
        # self.redis.hset("LAST_TRADE_TIME", self.market_code, data[-1]["time"])
        self.redis.hset(redis_key, symbol, data)

    def broadcast_data(self, data):
        # save_big_deals.delay(self.market_code, data)
        pass


class HuobiDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(HuobiDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class HuobiTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(HuobiTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.ltrim(redis_key, 1, 0)
        self.redis.rpush(redis_key, *data)
        self.redis.hset("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)


class ZBDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(ZBDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class ZBTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(ZBTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.ltrim(redis_key, 1, 0)
        self.redis.rpush(redis_key, *data)
        self.redis.set("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)


class HitBTCDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(HitBTCDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class HitBTCTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(HitBTCTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data):
        self.redis.ltrim(redis_key, 1, 0)
        self.redis.rpush(redis_key, *data)
        self.redis.set("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)


class OKEXDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(OKEXDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class OKEXTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(OKEXTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.ltrim(redis_key, 1, 0)
        self.redis.rpush(redis_key, *data)
        self.redis.set("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)

class OKCoinDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(OKCoinDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class OKCoinTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(OKCoinTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        return redis_key

    def save(self, redis_key, data, symbol=None):
        self.redis.ltrim(redis_key, 1, 0)
        self.redis.rpush(redis_key, *data)
        self.redis.set("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)


class PoloniexDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(PoloniexDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        # redis_key = "DEPTH_" + market_code.upper() + "_" + symbol
        redis_key = "depth:" + market_code
        return redis_key

    def save(self, redis_key, data, symbol=None):
        # self.redis.hset(redis_key, "bids", data["bids"])
        # self.redis.hset(redis_key, "asks", data["asks"])
        self.redis.hset(redis_key, symbol, data)

    def broadcast_data(self, data):
        pass


class PoloniexTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(PoloniexTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, symbol):
        # redis_key = "TRADE_" + market_code.upper() + "_" + symbol
        redis_key = "trade:" + market_code
        return redis_key

    def save(self, redis_key, data, symbol=None):
        # self.redis.ltrim(redis_key, 1, 0)
        # self.redis.rpush(redis_key, *data)
        # self.redis.set("LAST_TRADE_TIME", self.market_code, data[-1]["time"])
        # self.redis.hset(redis_key, symbol, data)
        pass

    def broadcast_data(self, data):
        # save_big_deals.delay(self.market_code, data)
        pass
