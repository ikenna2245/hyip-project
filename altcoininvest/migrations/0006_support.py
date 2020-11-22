# Generated by Django 3.1.2 on 2020-11-08 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('altcoininvest', '0005_comment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=120)),
                ('message', models.TextField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
