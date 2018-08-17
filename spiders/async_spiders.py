from celery_service.big_deals import save_big_deals
from core.base_spider import BaseSpider
import redisco


class BinanceDepthSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(BinanceDepthSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, url):
        coinpair = url.split("=")[-1].replace("/","_")
        redis_key = "DEPTH_" + market_code.upper() + "_" + coinpair
        return redis_key

    def save(self, redis_key, data):
        self.redis.hset(redis_key, "bids", data["bids"])
        self.redis.hset(redis_key, "asks", data["asks"])

    def broadcast_data(self, data):
        pass


class BinanceTradeSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(BinanceTradeSpider, self).__init__(*args, **kwargs)

    def get_redis_key(self,market_code, url):
        coinpair = url.split("=")[-1].replace("/", "_")
        redis_key = "TRADE_" + market_code.upper() + "_" + coinpair
        return redis_key

    def save(self, redis_key, data):
        self.redis.rpush(redis_key, *data)
        self.redis.hset("LAST_TRADE_TIME", self.market_code, data[-1]["time"])

    def broadcast_data(self, data):
        save_big_deals.delay(self.market_code, data)
