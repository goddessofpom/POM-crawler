from core.factory import AsyncioSpiderFactory
from component.cleaners import ZBTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import ZBTradeExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("ZB")
    ip_controller = StandardController()
    cleaner = ZBTradeCleaner()
    exception_handler = ZBTradeExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "ZBTradeSpider", "ZB", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "http://api.zb.cn/data/v1/trades?size=50&market="
    url_list = [[depth_url + coinpair.replace("/", "_").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()
