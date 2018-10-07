from core.factory import AsyncioSpiderFactory
from component.cleaners import BinanceTradeCleaner
from component.limiters import StandardLimiter
from component.ip_controllers import StandardController
from component.exception_handler import BinanceTradeExceptionHandler
import tracemalloc
import os

def display_top(snapshot, group_by='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(group_by)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno,
                 stat.size / 1024))

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


if __name__ == "__main__":
    limiter = StandardLimiter("Binance")
    cleaner = BinanceTradeCleaner()
    exception_handler = BinanceTradeExceptionHandler()
    ip_controller = StandardController()
    spider = AsyncioSpiderFactory.make_spider(
        "BinanceTradeSpider", "Binance", limiter=limiter, cleaner=cleaner,
        exception_handler=exception_handler, ip_controller=ip_controller
    )
    coinpairs = spider.get_coinpairs()
    depth_url = "https://api.binance.com/api/v1/trades?limit=100&symbol="
    url_list = [[depth_url + coinpair.replace("/", ""), coinpair] for coinpair in coinpairs]
    spider.add_task(url_list)

    spider.run()
