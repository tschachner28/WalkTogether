# Generated by Django 3.1.7 on 2021-03-19 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='times_available',
        ),
    ]
