from django.contrib import admin

from .models import Expenses


@admin.register(Expenses)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "time", "item", "cost")
    list_filter = ("user", "date", "time", "item", "cost")
    search_fields = ("date", "time", "item", "cost")
