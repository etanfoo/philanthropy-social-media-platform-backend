from django.db import models
from account.models import Account

# Create your models here.
class Post(models.Model):
    image_url = models.TextField(blank = True)
    account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    is_mission = models.BooleanField()
    dollar_target = models.IntegerField()
    current_dollar = models.IntegerField()

    def __str__(self):
        return self.title

    # do we need receiver?