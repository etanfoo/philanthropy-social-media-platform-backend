from django.db import models
from account.models import Account
from Post.models import Post
from django.utils import timezone

# Create your models here.
class Donate(models.Model):
    account_id_from = models.ForeignKey(Account, on_delete = models.CASCADE)
    post_id_to = models.ForeignKey(Post, on_delete = models.CASCADE)
    amount = models.IntegerField()
    is_recurring = models.BooleanField()
    start_date = models.DateTimeField(default = timezone.now)
    occurence = models.IntegerField(blank = True, null = True)
    times_donated = models.IntegerField(blank = True, default = 1)

    def __str__(self):
        return str(self.account_id_from.pk) + " " + str(self.post_id_to.pk) + " " + str(self.amount) + " " + str(self.start_date)

    # do we need receiver?