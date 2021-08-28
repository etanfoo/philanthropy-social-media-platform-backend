#from apscheduler.schedulers.background import BackgroundScheduler
from Post.models import Post
from Donate.models import Donate
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import math
#sched = BackgroundScheduler()
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes = 1)
def timed_job():
    #print('This job is run every 1 minute')
    all_donations = Donate.objects.all()
    for donation in all_donations:
        if (donation.is_recurring):
            cur_post = Post.objects.filter(pk=donation.post_id_to.pk).filter(is_mission=True).values('current_dollar')
            if (cur_post.exists()):
                #print(donation.start_date)
                #print(donation.occurence)
                x = datetime.datetime.now()
                #print(x)
                #print("subtracting times")
                newx = x.replace(tzinfo = None) - donation.start_date.replace(tzinfo = None)
                #print(newx)
                #print(newx.seconds % 60)
                #print((math.floor(newx.total_seconds()/60) - 600))
                #print((math.floor(newx.total_seconds()/60) - 600) % 60)
                #print(newx.days)
                #If i want to run everyday
                #if (newx.days % donation.occurence == 0):
                # if ((newx.seconds % 60) % donation.occurence == 0):
                if ((math.floor(newx.total_seconds()/60) - 600) % 60 == 0):
                    #print((newx.seconds % 60) % donation.occurence)
                    prev_current_dollar = cur_post[0]['current_dollar']
                    if (prev_current_dollar is None):
                        prev_current_dollar = 0
                    #print("Previous current dollar = ")
                    #print(cur_post[0]['current_dollar'])
                    cur_post.update(current_dollar = prev_current_dollar + donation.amount)
                    #donation.update(times_donated = donation.times_donated + 1)
                    donation.times_donated = donation.times_donated + 1
                    donation.save()
                    #print("printing current dollar")
                    #print(prev_current_dollar)
                    # print("donation amount is")
                    # print(donation.amount)
                    # print("times donated is")
                    # print(donation.times_donated)
                    # print("_____________________________")

sched.start()
