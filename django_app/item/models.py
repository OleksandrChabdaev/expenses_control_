from django.db import models
from django.db.models.functions import Lower
from user.models import User


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Item name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User id")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        constraints = [models.UniqueConstraint(Lower("name"), "user", name="unique")]
