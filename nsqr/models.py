from django.db import models

# Create your models here.


class Task(models.Model):
    address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    task_status = models.SmallIntegerField(choices=[(1, 'NOT_STARTED'), (2, 'PENDING'), (3, 'FINISHED')], default=1)

    def __str__(self):
        return f"{self.address} - {self.timestamp}"


class Result(models.Model):
    address = models.CharField(max_length=255)
    words_count = models.IntegerField()
    http_status = models.SmallIntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.address} - {self.words_count}"

