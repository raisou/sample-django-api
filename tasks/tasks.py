from time import sleep
from random import randint

from sample_api.celery import app


@app.task
def heavy_task():
    sleep(randint(60))  # Do some background jobs
    return 'heavy task executed successfully'


@app.task
def light_task():
    sleep(1)  # Do some background jobs
    return 'light task executed successfully'


@app.task
def random_task():
    sleep(randint(10, 60))  # Do some background jobs
    return 'random task executed successfully'
