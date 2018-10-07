from core.factory import AsyncioSpiderFactory
from component.cleaners import OKCoinDepthCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import OKCoinDepthExceptionHandler

if __name__ == "__main__":
    limiter = StandardLimiter("OKCOIN")
    ip_controller = StandardController()
    cleaner = OKCoinDepthCleaner()
    exception_handler = OKCoinDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "OKCoinDepthSpider", "OKCOIN", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "https://www.okcoin.com/api/v1/depth.do?symbol="
    url_list = [[depth_url + coinpair.replace("/", "_").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()