# Generated by Django 4.1.1 on 2022-11-03 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0011_alter_expenses_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='time',
            field=models.TimeField(default=datetime.time(6, 51, 17, 823068), verbose_name='Time'),
        ),
    ]
