from core.factory import AsyncioSpiderFactory
from component.cleaners import HitBTCTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import HitBTCTradeExceptionHandler
from core.config import AUTH_KEY


if __name__ == "__main__":
    limiter = StandardLimiter("HitBTC")
    ip_controller = StandardController()
    cleaner = HitBTCTradeCleaner()
    exception_handler = HitBTCTradeExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "HitBTCTradeSpider", "HitBTC", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://community-hitbtc.p.mashape.com/api/1/public/{}/trades"
    url_list = [[depth_url.format(coinpair.replace("/", "").upper()), coinpair] for coinpair in coinpairs]
    headers = {"X-Mashape-Key": AUTH_KEY["HitBTC"]["KEY"],"Accept": "application/json"}
    spider.add_task(url_list,headers=headers)

    spider.run()