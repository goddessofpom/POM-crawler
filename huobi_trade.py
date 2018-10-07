from core.factory import AsyncioSpiderFactory
from component.cleaners import HuobiTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import HuobiDepthExceptionHandler


if __name__ == "__main__":
    limiter = StandardLimiter("Huobi")
    ip_controller = StandardController()
    cleaner = HuobiTradeCleaner()
    exception_handler = HuobiDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "HuobiTradeSpider", "Huobi", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    trade_url = "https://api.huobi.pro/market/history/trade?size=100&symbol="
    url_list = [[trade_url + coinpair.replace("/", "").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()
