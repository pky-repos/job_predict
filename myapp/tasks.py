from celery import shared_task

from myapp.models import JobLog
from time import time
from celery.signals import task_prerun, task_postrun
import random


@shared_task
def job_predict_pending(pk):
    return random.random()


d = {}


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    print("task_prerun_handler", task, args, kwargs, extras)
    d[task_id] = time()
    job_log = JobLog.objects.filter(pk=args[0])
    print(job_log)


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **extras):
    print("task_postrun_handler", task, args, kwargs, retval, extras)

    try:
        cost = time() - d.pop(task_id)
    except KeyError:
        cost = -1

    job_log = JobLog.objects.filter(pk=args[0]).update(
        task_runtime=cost * 1000,
        task_status=state
    )
    print(job_log)
