# Generated by Django 3.1.7 on 2021-03-19 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20210319_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='walk_shifts',
            field=models.TextField(default=''),
        ),
    ]
