from django.contrib import admin
from .models import Blog, Comment, Support, Subscriber, FAQ, Ads

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Support)
admin.site.register(Subscriber)
admin.site.register(FAQ)
admin.site.register(Ads)
