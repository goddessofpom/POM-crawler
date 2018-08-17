import asyncio
import json
import time
import traceback
from component.log import get_logger
import aiohttp
import redis
import requests
import json

from core.config import REDIS_CONFIG, IP_CONFIG, GALAXY_CONFIG


class BaseSpider(object):

    def __init__(self, market_code, limiter, cleaner, exception_handler, ip_controller=None):
        self.task_url = []
        self.loop = asyncio.get_event_loop()
        self.limiter = limiter
        self.cleaner = cleaner
        self.ip_controller = ip_controller
        self.exception_handler = exception_handler
        self.market_code = market_code
        self.redis = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(
            REDIS_CONFIG['host'] + "/" + REDIS_CONFIG['db']
        ))
        self.fetch_count = 0
        self.logger = get_logger(self.market_code)

    def get_coinpairs(self):
        r = requests.post(GALAXY_CONFIG['host'] + "/api/coinpair/", timeout=10, data={
            "market_code": self.market_code
        })
        data = json.loads(r.content)["data"]["list"]
        coinpairs = [i["pair_name"] for i in data]
        return coinpairs

    async def _fetch(self, semaphore, url, symbol, timeout=10, ssl=None, headers=None, proxy=None):

        if self.ip_controller:
            local_addr = self.ip_controller.get_ip()
            if local_addr:
                session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
                    verify_ssl=False,force_close=True,local_addr=(local_addr, 0)
                ))
            else:
                self.logger.warning("No ip for using!!")
                time.sleep(IP_CONFIG['ip_retry_interval'])
                local_addr = self.ip_controller.get_ip()
                session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
                    verify_ssl=False, force_close=True, local_addr=(local_addr, 0)
                ))
        else:
            session = aiohttp.ClientSession()
            local_addr = None

        async with semaphore:
            async with session as session:
                try:
                    start_request_time = time.time()
                    async with session.get(url, timeout=timeout, ssl=ssl, proxy=proxy) as response:
                        text = await response.text()
                        if response.status == 200:
                            parse_data = json.loads(text)
                            self.logger.info("success:%s" % self.fetch_count)

                            is_correct = self.exception_handler.is_correct(self.market_code, parse_data)

                            if is_correct is True:

                                try:
                                    data = self.cleaner.clean_data(self.market_code, symbol, parse_data)
                                except:
                                    self.logger.error("unexcept except while clean data, DATA:%s" % parse_data)
                                    return False
                                redis_key = self.get_redis_key(self.market_code, url)

                                try:
                                    self.save(redis_key, data)
                                except:
                                    self.logger.error("unexcept error while saving data")
                                    print(traceback.print_exc())
                                    self.loop.stop()
                                
                                self.logger.info("success with url {}".format(url), text[:100])

                                try:
                                    self.broadcast_data(data)
                                except:
                                    self.logger.error("unexcept error while send data to celery")
                                    print(traceback.print_exc())
                                    self.loop.stop()
                                    
                                
                            else:
                                self.logger.warning("get wrong data, status:%s" % is_correct)
                                self.exception_handler.handle_exception(
                                    is_correct, ip_controller=self.ip_controller, ip=local_addr,
                                    spider_logger=self.logger
                                )

                        elif response.status == 400:
                            self.logger.warning("url:%s, coinpair dose not exist" % url)
                        else:
                            # print("faild with url {}".format(url), text)
                            self.logger.error("fetch url:%s failed,status_code:%s" % (url, response.status))

                        end_request_time = time.time()
                        response_time = end_request_time - start_request_time

                        # self.limiter.limit_per_request(url, response_time)

                        if self.fetch_count >= IP_CONFIG['reuse_ip_count'] and self.ip_controller:
                            self.ip_controller.reuse_ip()
                            self.fetch_count = 0
                        else:
                            self.fetch_count = self.fetch_count + 1
                        return text
                except asyncio.TimeoutError:
                    self.logger.error("asyncio timeout! url:%s" % (url,))
                    return None
                except Exception as e:
                    self.logger.error("unexcept error while fetching url!")
                    print(traceback.print_exc())
                    self.loop.stop()
                    return None

    def add_task(self, tasks):
        semaphore = asyncio.Semaphore(self.limiter.get_semaphore_concurrent())
        for task in tasks:
            self.task_url.append(self._fetch(semaphore,task[0], task[1]))

    def get_redis_key(self,market_code, url):
        self.logger.error("get_redis_key method must override")
        self.loop.stop()

    def save(self, redis_key, data):
        self.logger.error("save method must override")
        self.loop.stop()

    def broadcast_data(self, data):
        self.logger.error("broadcast_data method must override")
        self.loop.stop()


    def run(self):
        self.loop.run_until_complete(asyncio.ensure_future(asyncio.wait(self.task_url)))
        # self.loop.run_forever()
