from celery_service.config import MyTask
from celery_main import app
from celery.signals import worker_process_init, worker_process_shutdown, celeryd_init
import redis
from core.config import REDIS_CONFIG
from datafilter.big_deal_filter import BigDealFilter
import pymysql
from DBUtils.PooledDB import PooledDB
from core.config import MYSQL_CONFIG
import traceback


redis_con = None
conn = None


@worker_process_init.connect
def init_worker(**kwargs):
    global redis_con
    redis_con = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(
                    REDIS_CONFIG['host'] + "/" + REDIS_CONFIG['db']
                ))
    global conn
    conn = pymysql.connect(port=MYSQL_CONFIG['port'], user=MYSQL_CONFIG['user'], password=MYSQL_CONFIG["passwd"],
                           database=MYSQL_CONFIG['db'], charset=MYSQL_CONFIG['charset'], host=MYSQL_CONFIG['host'])

@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global conn
    if conn:
        conn.close()



@app.task(base=MyTask)
def save_big_deals(market_code ,data):
    fil = BigDealFilter(redis_con)
    """
    mysql_pool = PooledDB(
        pymysql, MYSQL_CONFIG['min_size'], host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'], passwd=MYSQL_CONFIG['passwd'], db=MYSQL_CONFIG['db'],
        port=MYSQL_CONFIG['port'], charset=MYSQL_CONFIG['charset']
    )
    """

    last_big_deal_time = redis_con.hget("LAST_TRADE_TIME",market_code) or 0
    save_data = fil.get_useful_data(data, int(last_big_deal_time))
    # conn = mysql_pool.connection()
    # conn = pymysql.connect(port=MYSQL_CONFIG['port'],user=MYSQL_CONFIG['user'],password=MYSQL_CONFIG["passwd"], database=MYSQL_CONFIG['db'],charset=MYSQL_CONFIG['charset'],host=MYSQL_CONFIG['host'])
    if save_data:
        cur = conn.cursor()
        sql = "INSERT INTO big_deal (timestamp, symbol, order_id, market_code, side, price, amount, cny_price, usd_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.executemany(sql,save_data)
            conn.commit()
        except:
            print(traceback.print_exc())
