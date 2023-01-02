from django.db import models


class JobLog(models.Model):
    id = models.IntegerField(primary_key=True)
    task_runtime = models.IntegerField(null=True)  # millisecond
    task_status = models.CharField(max_length=20, null=True)
    misc = models.JSONField(null=True)
