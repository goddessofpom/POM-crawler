from core.factory import AsyncioSpiderFactory
from component.cleaners import ZBDepthCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import ZBDepthExceptionHandler


if __name__ == "__main__":
    limiter = StandardLimiter("ZB")
    ip_controller = StandardController()
    cleaner = ZBDepthCleaner()
    exception_handler = ZBDepthExceptionHandler()

    spider = AsyncioSpiderFactory.make_spider(
        "ZBDepthSpider", "ZB", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )

    coinpairs = spider.get_coinpairs()
    depth_url = "http://api.zb.cn/data/v1/depth?size=50&market="
    url_list = [[depth_url + coinpair.replace("/", "_").lower(), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()
