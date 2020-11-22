from django.contrib import admin
from .models import Profile, Top_investor, Testimonial, AdminFact
# Register your models here.
admin.site.register(Profile)
admin.site.register(Top_investor)
admin.site.register(Testimonial)
admin.site.register(AdminFact)
