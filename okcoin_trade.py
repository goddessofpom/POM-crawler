from core.factory import AsyncioSpiderFactory
from component.cleaners import OKCoinTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import OKCoinTradeExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("OKCoin")
    ip_controller = StandardController()
    cleaner = OKCoinTradeCleaner()
    exception_handler = OKCoinTradeExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "OKCoinTradeSpider", "OKCoin", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://www.okcoin.com/api/v1/trades.do?symbol="
    url_list = [[depth_url + coinpair.replace("/", "_").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()