# Generated by Django 2.2 on 2020-04-01 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200401_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.CharField(default='', max_length=256),
        ),
    ]