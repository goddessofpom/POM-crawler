from core.config import IP_CONFIG
import time
from queue import PriorityQueue
import asyncio

class ScoreSession(object):
    def __init__(self, session, score=IP_CONFIG['max_request_per_min']):
        self.session = session
        self.score = score
        self.start_time = time.time()

    def __lt__(self, other):
        return self.score < other.score

    def get_fetch_session(self):
        now_time = time.time()

        if self.score <= 0:
            asyncio.sleep(IP_CONFIG['sleep_per_min'])

        if now_time - self.start_time >= 60:
            self.score = IP_CONFIG['max_request_per_min']
            self.start_time = now_time

        self.score = self.score - 1
        return self.session


class BaseController(object):
    def __init__(self):
        self.enable_sessions = PriorityQueue()
        self.disable_sessions = []

    def prepare_session(self, sessions):
        for se in sessions:
            init_session = ScoreSession(se)
            self.enable_sessions.put(init_session)


    def get_session(self):
        raise NotImplementedError("this method must override")


class StandardController(BaseController):
    def __init__(self):
        super(StandardController, self).__init__()

    def get_session(self):
        priority_session = self.enable_sessions.get()
        session = priority_session.get_fetch_session()
        self.enable_sessions.put(priority_session)
        return session

