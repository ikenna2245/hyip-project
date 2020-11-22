from django.db import models
from django.utils import timezone
# Create your models here.

class Blog(models.Model):
    image = models.ImageField(upload_to = 'blog')
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=120)
    about = models.TextField()
    roi = models.TextField()
    cash = models.TextField()
    deposit = models.TextField()

    def __str__(self):
         return f'{self.title}'

class Comment (models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    comment = models.TextField()
    approve = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.comment}'

class Support(models.Model):
    date = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=550)
    last_name = models.CharField(max_length=550)
    email= models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    status = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.first_name} - {self.last_name} : {self.subject}'

class Subscriber (models.Model):
    email = models.CharField(max_length=120)
    def __str__(self):
        return f'{self.email}'

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question}'

class Ads (models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    def __str__(self):
        return f'{self.title}'
