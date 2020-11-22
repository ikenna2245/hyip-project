# Generated by Django 3.1.3 on 2020-11-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_auto_20201115_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d_history',
            name='transaction_id',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='transaction_id',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
