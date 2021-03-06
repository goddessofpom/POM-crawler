from core.factory import AsyncioSpiderFactory
from component.cleaners import PoloniexTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import PoloniexTradeExceptionHandler
import time

if __name__ == "__main__":
    limiter = StandardLimiter("Poloniex")
    ip_controller = StandardController()
    cleaner = PoloniexTradeCleaner()
    exception_handler = PoloniexTradeExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "PoloniexTradeSpider", "Poloniex", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    end = int(time.time())
    start = end - 3600
    depth_url = "https://poloniex.com/public?command=returnTradeHistory&start=%s&end=%s&currencyPair=" % (start, end)
    url_list = [[depth_url + "_".join(coinpair.split("/")[::-1]), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()