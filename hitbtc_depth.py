from core.factory import AsyncioSpiderFactory
from component.cleaners import HitBTCDepthCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import HitBTCDepthExceptionHandler
from core.config import AUTH_KEY


if __name__ == "__main__":
    limiter = StandardLimiter("HitBTC")
    ip_controller = StandardController()
    cleaner = HitBTCDepthCleaner()
    exception_handler = HitBTCDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "HitBTCDepthSpider", "HitBTC", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://community-hitbtc.p.mashape.com/api/1/public/{}/orderbook"
    url_list = [[depth_url.format(coinpair.replace("/", "").upper()), coinpair] for coinpair in coinpairs]
    headers = {"X-Mashape-Key": AUTH_KEY["HitBTC"]["KEY"],"Accept": "application/json"}
    spider.add_task(url_list,headers=headers)

    spider.run()
