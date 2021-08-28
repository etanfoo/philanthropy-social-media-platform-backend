from django.db import models
from account.models import Account
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    creator = models.ForeignKey(Account, on_delete = models.CASCADE)
    title = models.TextField()
    location = models.TextField()
    date = models.DateTimeField()
    description = models.TextField()
    duration = models.IntegerField()
    event_pic = models.TextField(blank=True, null=True)
    participant_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.creator) + ", " + str(self.title)