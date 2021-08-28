from django.db import models
from account.models import Account
from event.models import Event

# Create your models here.
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    user_id = models.ForeignKey(Account, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.event) + ", " + str(self.user_id)