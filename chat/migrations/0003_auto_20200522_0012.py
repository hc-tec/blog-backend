# Generated by Django 2.2.5 on 2020-05-22 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatinfo_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatinfo',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='chatinfo',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
