from django.db import models
from account.models import Account
from Post.models import Post

# Create your models here.
class Post(models.Model):
    account_id_from = models.ForeignKey(Account, on_delete = models.CASCADE)
    post_id_to = models.ForeignKey(Post, on_delete = models.CASCADE)
    amount = models.IntegerField()
    is_recurring = models.BooleanField()
    start_date = models.DateField()
    occurence = models.IntegerField()
    times_donated = models.IntegerField()

    def __str__(self):
        return self.account_id_from + " " + self.post_id_to + " " + self.amount + " " + self.start_date

    # do we need receiver?