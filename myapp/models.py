from django.db import models


class JobLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    job_id = models.IntegerField()
    task_id = models.UUIDField(null=True)
    task_runtime = models.IntegerField(null=True)  # micro second
    task_status = models.CharField(max_length=20, null=True)
    misc = models.JSONField(null=True)
    job_started_at = models.DateTimeField(null=True)
    job_end_at = models.DateTimeField(null=True)

