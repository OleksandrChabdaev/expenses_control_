# Generated by Django 4.1.1 on 2022-11-02 07:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expenses',
            options={'ordering': ['-date', '-time'], 'verbose_name': 'Expenses'},
        ),
        migrations.RemoveField(
            model_name='expenses',
            name='date_time',
        ),
        migrations.AddField(
            model_name='expenses',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='expenses',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Time'),
        ),
    ]
