from core.factory import AsyncioSpiderFactory
from component.cleaners import BinanceCleaner
from component.limiters import BinanceLimiter
from component.ip_controllers import BinanceController
from component.exception_handler import BinanceExceptionHandler


if __name__ == "__main__":
    limiter = BinanceLimiter("Binance")
    cleaner = BinanceCleaner()
    exception_handler = BinanceExceptionHandler()
    spider = AsyncioSpiderFactory.make_spider(
        "BinanceDepthSpider", "Binance", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler
    )
    coinpairs = spider.get_coinpairs()
    depth_url = "https://api.binance.com/api/v1/depth?limit=100&symbol="
    url_list = [depth_url + coinpair.replace("/", "") for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()