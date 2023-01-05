from celery import shared_task
from django.db.models import F, Value
from celery.signals import task_prerun, task_postrun
from datetime import datetime

from myapp.models import JobLog


@shared_task
def job_predict_pending(pk):
    task_id = job_predict_pending.request.id

    mydict = {"foo": "bar"}

    job_log = JobLog.objects.filter(job_id=pk, task_id=task_id).update(
        misc=mydict
    )
    print(job_log)


@task_prerun.connect(sender=job_predict_pending)
def task_prerun_handler(signal, sender, task_id, task, args, kwargs, **extras):
    print("task_prerun_handler", task_id, task, args, kwargs, extras)

    job_log = JobLog.objects.create(job_id=args[0], task_id=task_id, job_started_at=datetime.now())
    print(job_log)


@task_postrun.connect(sender=job_predict_pending)
def task_postrun_handler(signal, sender, task_id, task, args, kwargs, retval, state, **extras):
    print("task_postrun_handler", task_id, task, args, kwargs, retval, extras)

    now = datetime.now()
    job_log = JobLog.objects.filter(job_id=args[0], task_id=task_id).update(
        task_status=state,
        job_end_at=now,
        task_runtime=Value(now) - F('job_started_at'),
    )
    print(job_log)
