from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    referral = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_referred', null= True, blank = True)
    address = models.CharField(max_length = 30, blank = True, null= True, default = "not defined")
    phone_number = models.CharField(max_length=15, blank = True, null=True, default = "not defined")
    city = models.CharField(max_length=25, blank = True, null= True, default = "not defined")
    state = models.CharField(max_length=25, blank = True, null= True, default = "not defined")
    country = models.CharField(max_length=54, null= True, blank =True)
    paypal = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    pexpay = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    perfectmoney = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    payza = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    hdmoney = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    egopay = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    okpay = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    solidtrustpay = models.FloatField(max_length=54, blank = True, null=True, default = 0)
    webmoney = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    bankwire = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    ethereum = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    bitcoin = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    bankwire = models.FloatField(max_length=15, blank = True, null= True, default = 0)
    pin = models.CharField(max_length=4, blank = True, null= True)

    def __str__(self):
        return f'{self.user.username} profile'

class Top_investor (models.Model):
    image = models.ImageField(upload_to = 'top_investors')
    name = models.CharField(max_length = 50)
    amount = models.CharField(max_length = 15)

    def __str__(self):
        return f'{self.name} - {self.amount} - {self.image.url}'

class Testimonial (models.Model):
    image = models.ImageField(upload_to = 'testimonials')
    name = models.CharField(max_length = 50)
    plan = models.CharField(max_length = 15)
    testimony = models.CharField(max_length = 250)

    def __str__(self):
        return f'{self.name} - {self.plan} - {self.testimony} -  {self.image.url}'

class AdminFact(models.Model):
    total_members = models.CharField(max_length=10)
    total_deposits = models.CharField(max_length=10)
    total_withdraw = models.CharField(max_length=10)
    days_online = models.CharField(max_length=10)
    registered_users = models.CharField(max_length=10)

    def __str__(self):
        return f'members: {self.total_members} - deposits: {self.total_deposits}'
