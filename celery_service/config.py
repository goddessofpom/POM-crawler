from celery.task import Task


BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_RESULT_EXPIRES = 1200 # celery任务执行结果的超时时间
CELERYD_CONCURRENCY = 50 # celery worker的并发数
CELERYD_PREFETCH_MULTIPLIER = 4 # celery worker 每次去取任务的数量
CELERYD_MAX_TASKS_PER_CHILD = 40 # 每个worker执行了多少任务就会死掉
CELERY_DEFAULT_QUEUE = "default_plugin" # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面

CELERY_IMPORTS = (
    'celery_service.big_deals'
)

CELERY_QUEUES = {
    'default_plugin': {
        'exchange': 'default_plugin',
        'exchange_type': 'direct',
        'routing_key': 'default'
    },
    'big_deal_plugin': {
        'exchange': 'big_deal_plugin',
        'exchange_type': 'topic',
        'routing_key': 'big_deal.#'
    },
    'wave_plugin': {
        'exchange': 'wave_plugin',
        'exchange_type': 'topic',
        'routing_key': 'wave.#'
    }
}

class MyRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith("big_deal"):
            return {
                'queue': 'big_deal_plugin'
            }
        elif task.startswith("wave"):
            return {
                'queue': 'wave_plugin'
            }
        else:
            return None

CELERY_ROUTES = (MyRouter(), )

class MyTask(Task):

    def on_success(self, retval, task_id, args, kwargs):
        print('task done: {0}'.format(retval))
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task fail, reason: {0}'.format(exc))
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)
