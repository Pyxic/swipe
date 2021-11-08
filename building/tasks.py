from datetime import date

from account.models import User
from building.models import Promotion
from swipe.celery import app
from celery.schedules import crontab


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('Hello'))

    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        check_promotion.s(),
    )

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        check_subscription.s(),
    )


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)


@app.task
def check_promotion():
    return Promotion.objects.filter(finished__lte=date.today()).delete()


@app.task
def check_subscription():
    users_with_subscription = User.objects.filter(subscribed=True,
                                                  end_date=date.today())
    for user in users_with_subscription:
        user.subscribed = False
        user.save()
