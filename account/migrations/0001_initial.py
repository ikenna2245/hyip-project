# Generated by Django 3.0 on 2020-10-22 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='testimonials')),
                ('name', models.CharField(max_length=50)),
                ('plan', models.CharField(max_length=15)),
                ('testimony', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Top_investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='top_investors')),
                ('name', models.CharField(max_length=50)),
                ('amount', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default='not defined', max_length=30, null=True)),
                ('phone_number', models.CharField(blank=True, default='not defined', max_length=15, null=True)),
                ('city', models.CharField(blank=True, default='not defined', max_length=25, null=True)),
                ('state', models.CharField(blank=True, default='not defined', max_length=25, null=True)),
                ('country', models.CharField(blank=True, max_length=54, null=True)),
                ('paypal', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('pexpay', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('perfectmoney', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('payza', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('hdmoney', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('egopay', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('okpay', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('solidtrustpay', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('webmoney', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('bankwire', models.CharField(blank=True, default='not defined', max_length=54, null=True)),
                ('pin', models.CharField(blank=True, max_length=4, null=True)),
                ('referral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_referred', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
