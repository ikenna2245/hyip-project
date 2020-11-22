from django.contrib import admin
from .models import Deposit, Transaction, Payment_Request, Tickets, D_History
# Register your models here.
admin.site.register(Deposit)
admin.site.register(Transaction)
admin.site.register(Payment_Request)
admin.site.register(Tickets)
admin.site.register(D_History)
