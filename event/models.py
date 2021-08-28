from django.db import models
from account.models import Account
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    creator = models.ForeignKey(Account, on_delete = models.CASCADE)
    title = models.TextField()
    location = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    description = models.TextField()
    duration = models.IntegerField()

    def __str__(self):
        return str(self.creator) + ", " + str(self.title)