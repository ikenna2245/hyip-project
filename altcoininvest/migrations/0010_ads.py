# Generated by Django 3.1.3 on 2020-11-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altcoininvest', '0009_auto_20201118_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
    ]
