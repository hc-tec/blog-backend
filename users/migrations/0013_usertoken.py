# Generated by Django 2.2 on 2020-04-02 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200401_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
