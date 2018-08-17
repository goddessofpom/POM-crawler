from core.factory import AsyncioSpiderFactory
from component.cleaners import BinanceTradeCleaner
from component.limiters import BinanceLimiter
from component.ip_controllers import BinanceController
from component.exception_handler import BinanceTradeExceptionHandler


if __name__ == "__main__":
    limiter = BinanceLimiter("Binance")
    cleaner = BinanceTradeCleaner()
    exception_handler = BinanceTradeExceptionHandler()
    spider = AsyncioSpiderFactory.make_spider(
        "BinanceTradeSpider", "Binance", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler
    )
    coinpairs = spider.get_coinpairs()
    depth_url = "https://api.binance.com/api/v1/trades?limit=100&symbol="
    url_list = [[depth_url + coinpair.replace("/", ""), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()