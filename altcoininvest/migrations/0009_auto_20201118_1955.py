# Generated by Django 3.1.3 on 2020-11-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('altcoininvest', '0008_subscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='support',
            name='first_name',
            field=models.CharField(max_length=550),
        ),
        migrations.AlterField(
            model_name='support',
            name='last_name',
            field=models.CharField(max_length=550),
        ),
    ]