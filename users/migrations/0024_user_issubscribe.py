# Generated by Django 2.2 on 2020-04-18 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20200417_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isSubscribe',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
