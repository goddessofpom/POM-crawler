from core.factory import AsyncioSpiderFactory
from component.cleaners import BinanceDepthCleaner
from component.limiters import BinanceLimiter
from component.ip_controllers import StandardController
from component.exception_handler import BinanceDepthExceptionHandler


if __name__ == "__main__":
    limiter = BinanceLimiter("Binance")
    cleaner = BinanceDepthCleaner()
    exception_handler = BinanceDepthExceptionHandler()
    ip_controller = StandardController()
    spider = AsyncioSpiderFactory.make_spider(
        "BinanceDepthSpider", "Binance", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )
    coinpairs = spider.get_coinpairs()
    depth_url = "https://api.binance.com/api/v1/depth?limit=100&symbol="
    url_list = [[depth_url + coinpair.replace("/", ""), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()