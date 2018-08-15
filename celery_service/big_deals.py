from celery_service.config import MyTask
from celery_main import app
from datafilter.big_deal_filter import BigDealFilter

@app.task(base=MyTask)
def save_big_deals(data):
    print(data)
