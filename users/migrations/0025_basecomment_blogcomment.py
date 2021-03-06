# Generated by Django 2.2 on 2020-04-27 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_user_issubscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('avatar', models.CharField(blank=True, max_length=128, null=True)),
                ('message', models.CharField(max_length=1024)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('replied_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('basecomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseComment')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Blog')),
                ('multiple_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.BlogComment')),
            ],
            bases=('users.basecomment',),
        ),
    ]
