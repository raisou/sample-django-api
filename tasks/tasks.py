from random import randint
from time import sleep

from sample_api.celery_app import app


@app.task
def heavy_task(name: str = "heavy_task") -> str:  # noqa: ARG001
    sleep(randint(60, 70))  # Do some background jobs
    return "heavy task executed successfully"


@app.task
def light_task(name: str = "light_task") -> str:  # noqa: ARG001
    sleep(randint(1, 2))  # Do some background jobs
    return "light task executed successfully"


@app.task
def random_task(name: str = "random_task") -> str:  # noqa: ARG001
    sleep(randint(10, 60))  # Do some background jobs
    return "random task executed successfully"
