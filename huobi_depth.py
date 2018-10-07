from core.factory import AsyncioSpiderFactory
from component.cleaners import HuobiDepthCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import HuobiDepthExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("Huobi")
    ip_controller = StandardController()
    cleaner = HuobiDepthCleaner()
    exception_handler = HuobiDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "HuobiDepthSpider", "Huobi", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://api.huobi.pro/market/depth?type=step1&symbol="
    url_list = [[depth_url + coinpair.replace("/", "").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()
