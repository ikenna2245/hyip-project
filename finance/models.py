from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
def seven_days_hence():
    return timezone.now() + timezone.timedelta(days=5)

class Deposit (models.Model):
    transaction_id = models.CharField(max_length= 225 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    mature_date= models.DateTimeField(default=seven_days_hence)
    amount = models.FloatField(max_length=15, null=True, blank=True,)
    currency = models.CharField(max_length=15, default="dollar", null=True, blank=True,)
    plan = models.CharField(max_length=30, null=True, blank=True,)
    payment_mode = models.CharField(max_length=30, default= "paypal", null=True, blank=True,)
    status = models.BooleanField(default = False)
    matured = models.BooleanField(default = False)
    active_deposit = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    mature_deposit = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    total_payout = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    pending_payout = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    interest_today = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    interest_earnings = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    earning_today = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    total_earning = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)
    referral = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referral')
    referral_interest = models.FloatField(max_length=15, null=True, blank=True, default = 0.0)


    def __str__ (self):
        return f'{self.user} deposited {self.amount} - {self.currency} - ready on {self.mature_date}'

class D_History (models.Model):
    transaction_id = models.CharField(max_length= 225 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    mature_date= models.DateTimeField(default=seven_days_hence)
    amount = models.FloatField(max_length=15)
    currency = models.CharField(max_length=15, default="dollar")
    plan = models.CharField(max_length=30)
    payment_mode = models.CharField(max_length=30, default= "paypal")
    status = models.BooleanField(default = False)
    matured = models.BooleanField(default = False)
    def __str__(self):
        return f'{self.user.username} - {self.amount}'

class Payment_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(max_length=15)
    payment_mode = models.CharField(max_length=30, default= "paypal")
    account_id =  models.CharField(max_length=125)
    status = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.account_id} -- {self.amount} -- via {self.payment_mode}'

class Transaction (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    transaction_id  = models.CharField(max_length=225, null=True, blank=True)
    description = models.CharField(max_length=35, null=True)
    amount = models.FloatField(max_length=15)
    payment_mode = models.CharField(max_length=30, default= "paypal")
    approved = models.BooleanField(default = True)

    def __str__ (self):
        return f'{self.user.username} - {self.amount} - {self.payment_mode}'

class Tickets (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=50)
    contact_no = models.CharField(max_length = 20)
    description = models.TextField(max_length=50)
    status = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.user.username} -- {self.subject} -- {self.description}'
