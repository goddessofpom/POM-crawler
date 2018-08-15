from celery import Celery

app = Celery('data_service')
app.config_from_object('celery_service.config')
