from celery import shared_task
from django.db.models import F, Value

from myapp.models import JobLog
from time import time
from celery.signals import task_prerun, task_postrun
import random
from datetime import datetime


@shared_task
def job_predict_pending(pk):
    return random.random()


# d = {}


@task_prerun.connect
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    print("task_prerun_handler", task, args, kwargs, extras)
    # d[task_id] = time()
    job_log = JobLog.objects.create(job_id=args[0], task_id=task_id, job_started_at=datetime.now())
    print(job_log)


@task_postrun.connect
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **extras):
    print("task_postrun_handler", task, args, kwargs, retval, extras)
    #
    # try:
    #     cost = time() - d.pop(task_id)
    # except KeyError:
    #     cost = -1

    now = datetime.now()
    job_log = JobLog.objects.filter(job_id=args[0], task_id=task_id).update(
        task_status=state,
        job_end_at=now,
        task_runtime=Value(now) - F('job_started_at'),
    )
    print(job_log)
