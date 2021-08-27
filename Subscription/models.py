from django.db import models
from account.models import Account

# Create your models here.
class Subscription(models.Model):
    from_account_id = models.ForeignKey(Account, on_delete = models.CASCADE)
    to_account_id = models.ForeignKey(Account, on_delete = models.CASCADE)

    def __str__(self):
        return self.from_account_id + " " + self.to_account_id