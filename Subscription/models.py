from django.db import models
from account.models import Account

# Create your models here.
class Subscription(models.Model):
    from_account_id = models.ForeignKey(Account, related_name = "from_account_id", on_delete = models.CASCADE)
    to_account_id = models.ForeignKey(Account, related_name = "to_account_id", on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_account_id','to_account_id'],  name="unique_followers")
        ]

    def __str__(self):
        return str(self.from_account_id) + " -> " + str(self.to_account_id)