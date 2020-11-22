from django.urls import path
from . import views

urlpatterns = [
    path("make-deposit/", views.make_deposit, name="make_deposit"),
    path("make-deposit/checkout/", views.checkout, name="checkout"),
    path("make-deposit/checkout/ipn/confirm/payment/", views.ipn_view, name="ipn_view"),
    path("deposit-list/", views.deposit_list, name="deposit_list"),
    path("payment-request/", views.payment_request, name="payment_request"),
    path("all-transactions/", views.all_transactions, name="all_transactions"),
    path("deposit-history/", views.deposit_history, name="deposit_history"),
    path("earnings-history/", views.earnings_history, name="earnings_history"),
    path("tickets/", views.tickets, name="tickets"),
    path("referrals/", views.referrals, name="referrals"),
    path("referral-earnings/", views.referral_earnings, name="referral_earnings"),
]
