# Generated by Django 2.2.5 on 2020-05-22 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatinfo',
            name='user_name',
            field=models.CharField(default='', max_length=20),
        ),
    ]