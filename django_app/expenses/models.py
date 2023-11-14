from django.db import models
from django.utils import timezone
from item.models import Item
from user.models import User


def get_now_date():
    return timezone.localtime(timezone.now()).date()


def get_now_time():
    return timezone.localtime(timezone.now()).time().strftime("%H:%M:%S")


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User id")
    date = models.DateField(default=get_now_date, verbose_name="Date")
    time = models.TimeField(default=get_now_time, verbose_name="Time")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    cost = models.FloatField(verbose_name="Cost")

    class Meta:
        verbose_name = "Expenses"
        ordering = ["-date", "-time"]
