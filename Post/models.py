from django.db import models
from account.models import Account
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    image_url = models.TextField(blank = True)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    is_mission = models.BooleanField()
    is_shared = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True, default = None)
    time_created = models.DateTimeField(default = timezone.now)
    dollar_target = models.IntegerField(blank = True)
    current_dollar = models.IntegerField(blank = True, default = 0)

    def __str__(self):
        return self.title

    # do we need receiver?