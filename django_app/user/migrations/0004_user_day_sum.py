# Generated by Django 4.1.1 on 2022-10-26 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='day_sum',
            field=models.FloatField(default=0, verbose_name='Day sum'),
        ),
    ]
