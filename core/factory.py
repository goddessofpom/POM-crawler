class AsyncioSpiderFactory(object):
    @classmethod
    def make_spider(cls, spider_name,market_code, limiter, cleaner, exception_handler, ip_controller=None):
        try:
            spider_package = __import__("spiders.async_spiders", fromlist=True)
            temp_class = getattr(spider_package, spider_name)
        except AttributeError:
            raise AttributeError("don't have this spider")
        return temp_class(
            market_code=market_code,limiter=limiter, cleaner=cleaner,
            ip_controller=ip_controller, exception_handler=exception_handler
        )
