# Generated by Django 2.2 on 2020-04-01 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200401_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='friend_card',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
