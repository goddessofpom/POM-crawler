import asyncio
import json
import time
import traceback
from component.log import get_logger
import aiohttp
import redis
import requests
import json

from core.config import REDIS_CONFIG, IP_CONFIG, GALAXY_CONFIG, LIMITER_CONFIG


class BaseSpider(object):

    def __init__(self, market_code, limiter, cleaner, exception_handler, ip_controller):
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
        self.logger = get_logger(self.market_code)
        self.sessions = []

        semaphore = asyncio.Semaphore(self.limiter.get_semaphore_concurrent())

        for ip in IP_CONFIG['ip_list']:
            session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(verify_ssl=False, force_close=True, local_addr=(ip, 0)))
            self.sessions.append(session)

        self.ip_controller.prepare_session(self.sessions)

    def get_coinpairs(self):
        r = requests.post(GALAXY_CONFIG['host'] + "/api/coinpair/", timeout=10, data={
            "market_code": self.market_code
        })
        data = json.loads(r.content)["data"]["list"]
        coinpairs = [i["pair_name"] for i in data]
        return coinpairs

    async def _fetch(self, session, url, symbol, timeout=30, ssl=None, headers=None):
        """
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
        """

        try:
            start_request_time = time.time()
            async with session.get(url, timeout=LIMITER_CONFIG[self.market_code]['time_out'], ssl=ssl, proxy=None) as response:
                text = await response.text()
                parse_data = json.loads(text)
                if response.status == 200:
                    self.logger.info("success")

                    is_correct = self.exception_handler.is_correct(self.market_code, parse_data)

                    if is_correct is True:

                        try:
                            data = self.cleaner.clean_data(self.market_code, symbol, parse_data)
                        except:
                            self.logger.error("unexcept except while clean data, DATA:%s" % parse_data)
                            return False
                        redis_key = self.get_redis_key(self.market_code, symbol)

                        try:
                            self.save(redis_key, data, symbol=symbol)
                        except:
                            self.logger.error("unexcept error while saving data")
                            print(traceback.print_exc())
                            self.loop.stop()
                                
                            # self.logger.info("success with url {}".format(url), text[:100])
                            # self.logger.info("success")

                        try:
                            self.broadcast_data(data)
                        except:
                            self.logger.error("unexcept error while send data to celery")
                            print(traceback.print_exc())
                            self.loop.stop()
                                    
                                
                    else:
                        self.logger.warning("get wrong data, status:%s" % is_correct)
                        self.exception_handler.handle_exception(
                            self.logger, is_correct
                        )

                elif response.status == 400:
                    self.logger.warning("url:%s, coinpair dose not exist" % url)
                else:
                    # print("faild with url {}".format(url), text)
                    self.logger.error("fetch url:%s failed,status_code:%s" % (url, response.status))
                    except_type = self.exception_handler.is_correct(self.market_code, parse_data)
                    self.exception_handler.handle_exception(self.logger, except_type)

                end_request_time = time.time()
                response_time = end_request_time - start_request_time

                self.limiter.limit_per_request(symbol, response_time)

                asyncio.run_coroutine_threadsafe(self._fetch(session, url, symbol), self.loop)
                return text
        except asyncio.TimeoutError:
            self.logger.error("asyncio timeout! url:%s" % (url,))
            asyncio.run_coroutine_threadsafe(self._fetch(session, url, symbol), self.loop)
            return None
        except Exception as e:
            self.logger.error("unexcept error while fetching url!")
            print(traceback.print_exc())
            # self.loop.stop()
            return None

    def add_task(self, tasks, headers=None):
        for task in tasks:
            session = self.ip_controller.get_session()
            self.task_url.append(self._fetch(session, task[0], task[1], headers=headers))

    def get_redis_key(self,market_code, symbol):
        self.logger.error("get_redis_key method must override")
        self.loop.stop()

    def save(self, redis_key, data, symbol=None):
        self.logger.error("save method must override")
        self.loop.stop()

    def broadcast_data(self, data):
        self.logger.error("broadcast_data method must override")
        self.loop.stop()


    def run(self):
        self.loop.run_until_complete(asyncio.ensure_future(asyncio.wait(self.task_url)))
        self.loop.run_forever()
