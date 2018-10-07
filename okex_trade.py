from core.factory import AsyncioSpiderFactory
from component.cleaners import OKEXTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import OKEXTradeExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("OKEX")
    ip_controller = StandardController()
    cleaner = OKEXTradeCleaner()
    exception_handler = OKEXTradeExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "OKEXTradeSpider", "OKEX", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://www.okex.com/api/v1/trades.do?symbol="
    url_list = [[depth_url + coinpair.replace("/", "_").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()