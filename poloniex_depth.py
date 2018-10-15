from core.factory import AsyncioSpiderFactory
from component.cleaners import PoloniexDepthCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import PoloniexDepthExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("Poloniex")
    ip_controller = StandardController()
    cleaner = PoloniexDepthCleaner()
    exception_handler = PoloniexDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "PoloniexDepthSpider", "Poloniex", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://poloniex.com/public?command=returnOrderBook&depth=30&currencyPair="
    url_list = [[depth_url + "_".join(coinpair.split("/")[::-1]), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()