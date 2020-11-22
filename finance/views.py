from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import requests
from django.utils import timezone
from django.utils.crypto import get_random_string
from decimal import Decimal
from django_coinpayments.models import Payment
from django_coinpayments.exceptions import CoinPaymentsProviderError
from django.http.response import HttpResponseBadRequest
from django.conf import settings
from .utils import create_ipn_hmac
import logging
from .models import Deposit, Payment_Request, Transaction, D_History, Tickets
from account.models import Profile
from account.tasks import send_transaction_email_task

logger = logging.getLogger(__name__) 
  
# Create your views here.
@login_required()
def make_deposit (request):
    context = {
    "title": "Make Deposit",
    "deposits": Deposit.objects.filter(user=request.user.id, matured =True)
    }
    if request.method == 'POST':
        plan = request.POST.get('plan')
        payment_gateway = request.POST.get('payment_gateway')
        amount = float(request.POST.get('amount'))
        id = get_random_string(17).upper()
        if payment_gateway == "balance":
            balance = Deposit.objects.get(pk=request.POST.get('balance'))
            if amount <= balance.total_earning:
                if plan == "Basic" and amount >= float(100):
                    mature_date = timezone.now() + timezone.timedelta(days=3)
                    new_deposit = Deposit(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                         date=timezone.now(), plan=plan,
                                         mature_date=mature_date, status= True)
                    new_deposit.save()
                    send_transaction_email_task.delay(request.user.email, 'Deposit', id, payment_gateway, amount)
                    new_D_History = D_History(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                         date=timezone.now(), plan=plan,
                                         mature_date=mature_date, status= True)
                    new_D_History.save()
                    transaction = Transaction(user= request.user,
                                            transaction_id = id,
                                            amount = amount,
                                            description = "Deposit",
                                            payment_mode = payment_gateway, approved = True)
                    transaction.save()
                    balance.amount = balance.amount - amount
                    balance.save()
                    messages.success(request, "Deposit Succesful")
                    return render(request, "account/my_account.html")
                else:
                    messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                    return render(request, 'finance/make_deposit.html', context)
                if plan == "Business" and amount >= float(5000):
                    mature_date = timezone.now() + timezone.timedelta(days=6)
                    new_deposit = Deposit(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                        date=timezone.now(), plan=plan,
                                        mature_date=mature_date, status= True)
                    new_deposit.save()
                    send_transaction_email_task.delay(request.user.email, 'Deposit', id, payment_gateway, amount)
                    new_D_History = D_History(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                         date=timezone.now(), plan=plan,
                                         mature_date=mature_date, status= True)
                    new_D_History.save()
                    transaction = Transaction(user= request.user,
                                            transaction_id = id,
                                            amount = amount,
                                            description = "Deposit",
                                            payment_mode = payment_gateway, approved = True)
                    transaction.save()
                    balance.amount = balance.amount - amount
                    balance.save()
                    messages.success(request, "Deposit Succesful")
                    return render(request, "account/my_account.html")
                else:
                    messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                    return render(request, 'finance/make_deposit.html', context)
                if plan == "Index" and amount >= float(10000):
                    mature_date = timezone.now() + timezone.timedelta(days=8)
                    new_deposit = Deposit(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                        date=timezone.now(), plan=plan,
                                        mature_date=mature_date, status= True)
                    new_deposit.save()
                    send_transaction_email_task.delay(request.user.email, 'Deposit', id, payment_gateway, amount)
                    new_D_History = D_History(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                         date=timezone.now(), plan=plan,
                                         mature_date=mature_date, status= True)
                    new_D_History.save()
                    transaction = Transaction(user= request.user,
                                            transaction_id = id,
                                            amount = amount,
                                            description = "Deposit",
                                            payment_mode = payment_gateway, approved = True)
                    transaction.save()
                    balance.amount = balance.amount - amount
                    balance.save()
                    messages.success(request, "Deposit Succesful")
                    return render(request, "account/my_account.html")
                else:
                    messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                    return render(request, 'finance/make_deposit.html', context)
                if plan == "Dynamic" and amount >= float(50000):
                    mature_date = timezone.now() + timezone.timedelta(days=1)
                    new_deposit = Deposit(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                        date=timezone.now(), plan=plan,
                                        mature_date=mature_date, status= True)
                    new_deposit.save()
                    send_transaction_email_task.delay(request.user.email, 'Deposit', id, payment_gateway, amount)
                    new_D_History = D_History(user=request.user, amount=amount,
                                        payment_mode=payment_gateway, transaction_id=id,
                                         date=timezone.now(), plan=plan,
                                         mature_date=mature_date, status= True)
                    new_D_History.save()
                    transaction = Transaction(user= request.user,
                                            transaction_id = id,
                                            amount = amount,
                                            description = "Deposit",
                                            payment_mode = payment_gateway, approved = True)
                    transaction.save()
                    balance.amount = balance.amount - amount
                    balance.save()
                    messages.success(request, "Deposit Succesful")
                    return render(request, "account/my_account.html")
                else:
                    messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                    return render(request, 'finance/make_deposit.html', context)
            else:
                messages.info(request, "Insufficient Funds: the amount you wish to withdraw is more than your available balance")
                return render(request, 'finance/make_deposit.html', context)
        if payment_gateway == "PayPal":
            if plan == "Basic" and amount >= float(100):
                request.session['plan'] = plan
                request.session['amount'] = amount
                return redirect('checkout')
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Business" and amount >= float(5000):
                request.session['plan'] = plan
                request.session['amount'] = amount
                return redirect('checkout')
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Index" and amount >= float(10000):
                request.session['plan'] = plan
                request.session['amount'] = amount
                return redirect('checkout')
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Dynamic" and amount >= float(50000):
                request.session['plan'] = plan
                request.session['amount'] = amount
                return redirect('checkout')
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
        if payment_gateway == "Bitcoin":
            ref_int = amount * 15 /100
            parameters = { 'currency':'USD',
                        'value': amount}
            response = requests.get("https://blockchain.info/tobtc?",  params=parameters)
            amountBTC = Decimal(response.json())
            if plan == "Basic" and amount >= float(100):
                mature_date = timezone.now() + timezone.timedelta(days=3)
                payment = Payment(currency_original='btc',
                          currency_paid='btc',
                          amount=amountBTC,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency = 'Bitcoin')
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Bitcoin')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Business" and amount >= float(5000):
                mature_date = timezone.now() + timezone.timedelta(days=6)
                payment = Payment(currency_original='btc',
                          currency_paid='btc',
                          amount=amountBTC,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency = 'Bitcoin')
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Bitcoin')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Index" and amount >= float(10000):
                mature_date = timezone.now() + timezone.timedelta(days=8)
                payment = Payment(currency_original='btc',
                          currency_paid='btc',
                          amount=amountBTC,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency = 'Bitcoin')
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Bitcoin')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Dynamic" and amount >= float(50000):
                mature_date = timezone.now() + timezone.timedelta(days=1)
                payment = Payment(currency_original='btc',
                          currency_paid='btc',
                          amount_paid=Decimal(0),
                          amount=amountBTC,
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency = 'Bitcoin')
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Bitcoin')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
        if payment_gateway == "Ethereum":
            ref_int = amount * 15/100
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
            data = response.json()
            amountETH =  Decimal(amount / float(data['ethereum']['usd']))
            if plan == "Basic" and amount >= float(100):
                mature_date = timezone.now() + timezone.timedelta(days=3)
                payment = Payment(currency_original='eth',
                          currency_paid='btc',
                          amount=amountETH,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency="Ethereum")
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Ethereum')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Business" and amount >= float(5000):
                mature_date = timezone.now() + timezone.timedelta(days=6)
                payment = Payment(currency_original='eth',
                          currency_paid='btc',
                          amount=amountETH,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, referral_interest=ref_int, referral = request.user.profile.referral, currency="Ethereum")
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Ethereum')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Index" and amount >= float(10000):
                mature_date = timezone.now() + timezone.timedelta(days=8)
                payment = Payment(currency_original='eth',
                          currency_paid='btc',
                          amount=amountETH,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency="Ethereum", referral = request.user.profile.referral, referral_interest=ref_int)
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Ethereum')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)
            if plan == "Dynamic" and amount >= float(50000):
                mature_date = timezone.now() + timezone.timedelta(days=1)
                payment = Payment(currency_original='eth',
                          currency_paid='btc',
                          amount=amountETH,
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING)
                new_deposit = Deposit(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency="Ethereum", referral = request.user.profile.referral, referral_interest=ref_int)
                new_D_History = D_History(user=request.user, amount=amount,
                                    payment_mode=payment_gateway, plan=plan,
                                    mature_date=mature_date, currency = 'Ethereum')
                return create_tx(request, payment, new_deposit, new_D_History)
            else:
                messages.info(request, "Plan Error: Amount entered is less than the required amount for this plan.")
                return render(request, 'finance/make_deposit.html', context)

    else:
        return render(request, 'finance/make_deposit.html', context)
    return render(request, 'finance/make_deposit.html', context)

@login_required()
def checkout (request):
    if request.method == 'POST':
        body = json.loads(request.body)
        plan = body['plan']
        payment_mode = 'paypal'
        amount = float(body['amount'])
        ref_int = amount * 15/100
        balance = Profile.objects.get(user=request.user.id)
        balance.paypal += amount
        balance.save()
        id = body['data']['orderID']
        transaction = Transaction(user= request.user, transaction_id = id, amount = amount, description = "Deposit")
        transaction.save()
        if plan == "Basic":
            mature_date = timezone.now() + timezone.timedelta(days=3)
            new_deposit = Deposit(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                 date=timezone.now(), plan=plan, referral_interest=ref_int, mature_date=mature_date, referral = request.user.profile.referral, status= True,)
            new_deposit.save()
            send_transaction_email_task.delay(request.user.email, "Deposit", id, payment_mode, amount)
            new_D_History = D_History(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                 date=timezone.now(), plan=plan,mature_date=mature_date, status= True)
            new_D_History.save()
        if plan == "Business":
            mature_date = timezone.now() + timezone.timedelta(days=6)
            new_deposit = Deposit(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                date=timezone.now(), referral_interest=ref_int, referral = request.user.profile.referral, plan=plan, mature_date=mature_date, status= True)
            new_deposit.save()
            send_transaction_email_task.delay(request.user.email, "Deposit", id, payment_mode, amount)
            new_D_History = D_History(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                 date=timezone.now(), plan=plan,mature_date=mature_date, status= True)
            new_D_History.save()
        if plan == "Index":
            mature_date = timezone.now() + timezone.timedelta(days=8)
            new_deposit = Deposit(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                date=timezone.now(), referral_interest=ref_int, plan=plan, referral = request.user.profile.referral, mature_date=mature_date, status= True)
            new_deposit.save()
            send_transaction_email_task.delay(request.user.email, "Deposit", id, payment_mode, amount)
            new_D_History = D_History(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                 date=timezone.now(), plan=plan,mature_date=mature_date, status= True)
            new_D_History.save()
        if plan == "Dynamic":
            mature_date = timezone.now() + timezone.timedelta(days=1)
            new_deposit = Deposit(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                date=timezone.now(), plan=plan, referral_interest=ref_int, mature_date=mature_date, status= True, referral = request.user.profile.referral,)
            new_deposit.save()
            send_transaction_email_task.delay(request.user.email, "Deposit", id, payment_mode, amount)
            new_D_History = D_History(user=request.user, amount=amount,
                                payment_mode=payment_mode, transaction_id=id,
                                 date=timezone.now(), plan=plan, referral_interest=ref_int, mature_date=mature_date, status= True)
            new_D_History.save()
        return JsonResponse('Payment Completed!', safe=False)
    return render (request, 'finance/checkout.html')

@login_required()
def deposit_list (request):
    context = {
    "title": "Deposit List",
    "active_deposits" : Deposit.objects.filter(user=request.user.id, status = True),
    "matured_deposits" : Deposit.objects.filter(user=request.user.id, matured = True),
    }
    return render (request, 'finance/deposit_list.html', context)

@login_required()
def payment_request (request):
    if request.method == 'POST':
        payment_gateway = request.POST.get('payment_gateway')
        amount = float(request.POST.get('amount'))
        account_id = request.POST.get('account_id')
        type = request.POST.get('type')
        working_deposit = Deposit.objects.get(pk=request.POST.get('deposit'))
        if type == "investment":
            if amount <= working_deposit.total_earning:
                p_request = Payment_Request(user=request.user,
                                            amount = amount,
                                            account_id = account_id,
                                            payment_mode = payment_gateway)
                p_request.save()
                if working_deposit.payment_mode == "paypal":
                    balance = Profile.objects.get(user=request.user.id)
                    balance.paypal = balance.paypal - amount
                    balance.save()
                working_deposit.amount = working_deposit.amount - amount
                working_deposit.save()
                id = get_random_string(17).upper()
                transaction = Transaction(user= request.user,
                                        payment_mode= payment_gateway,
                                        transaction_id= id,
                                        amount= amount,
                                        description= "Withdraw", approved = True)
                transaction.save()
                send_transaction_email_task.delay(request.user.email, 'Withdrawal', id, payment_gateway, amount)
                messages.success(request, "Successful: Payment Request Sent")
                return redirect ('dashboard')
            else:
                messages.info(request, "Insufficient Funds: the amount you wish to withdraw is more than your available balance")
                return render(request, 'finance/payment_request.html')
        if type == "referral":
            if amount <= working_deposit.referral_interest:
                p_request = Payment_Request(user=request.user,
                                            amount = amount,
                                            account_id = account_id,
                                            payment_mode = payment_gateway)
                p_request.save()
                working_deposit.referral_interest = working_deposit.referral_interest - amount
                working_deposit.save()
                id = get_random_string(17).upper()
                transaction = Transaction(user= request.user,
                                        payment_mode= payment_gateway,
                                        transaction_id= id,
                                        amount= amount,
                                        description= "Referral", approved = True)
                transaction.save()
                send_transaction_email_task.delay(request.user.email, 'Referral Commission', id, payment_gateway, amount)
                messages.success(request, "Successful: Payment Request Sent")
                return redirect ('dashboard')
            else:
                messages.info(request, "Insufficient Funds: the amount you wish to withdraw is more than your available balance")
                return render(request, 'finance/payment_request.html')
    else:
        context = {
        "title": "Payment Request",
        "deposits": Deposit.objects.filter(user=request.user.id, matured =True),
        "referrals": Deposit.objects.filter(referral = request.user)
        }
        return render (request, 'finance/payment_request.html', context)

@login_required()
def all_transactions (request):
    context = {
    "title": "All Transactions",
    "transactions": Transaction.objects.filter(user=request.user)
    }
    return render(request, 'finance/all_transactions.html', context)

@login_required()
def deposit_history (request):
    context = {
    "title": "Deposit History",
    "deposits": D_History.objects.filter(user=request.user.id).order_by('-date')
    }
    return render(request, 'finance/deposit_history.html', context)

@login_required()
def earnings_history (request):
    context = {
    "title": "Earnings History",
    "earnings": Transaction.objects.filter(user=request.user).exclude(description='Deposit')
    }
    return render(request, 'finance/earnings_history.html', context)

@login_required()
def tickets (request):
    if request.method == 'POST':
        subject = request.POST.get("subject")
        phone = request.POST.get("phone")
        description = request.POST.get("message")
        ticket = Tickets(user=request.user, subject=subject, contact_no=phone, description = description)
        ticket.save()
        messages.success(request, "Ticket Created Successfully")
        return redirect ("tickets")
    context = {
    "title": "Tickets",
    "tickets": Tickets.objects.filter(user=request.user.id)
    }
    return render(request, 'finance/tickets.html', context)

@login_required()
def referrals (request):
    referral = Profile.objects.filter(referral=request.user.id)
    referral_deposit = 0.0
    ref_deposit = Deposit.objects.filter(user=request.user.profile.user)
    for ref in ref_deposit:
        referral_deposit += ref.amount
    context = {
    "title": "Referrals",
    "referral_count": referral.count(),
    "referral_deposit": referral_deposit,
    "referral": referral,
    }
    return render(request, 'finance/referrals.html', context)

@login_required()
def referral_earnings (request):
    ref_earnings = Transaction.objects.filter(description = "Referral")
    context = {
    "title": "Referral Earnings",
    "ref_earnings": ref_earnings
    }
    return render(request, 'finance/referral_earnings.html', context)

@login_required
def create_tx(request, payment, new_deposit, new_D_History):
    context = {}
    try:
        tx = payment.create_tx()
        payment.status = Payment.PAYMENT_STATUS_PENDING
        payment.save()
        t = Transaction(user=request.user, transaction_id=payment.provider_tx, amount = payment.amount, description="Deposit", approved=False, payment_mode = "Bitcoin")
        t.save()
        new_deposit.transaction_id = payment.provider_tx
        new_D_History.transaction_id = payment.provider_tx
        new_deposit.save()
        new_D_History.save()
        context['object'] = payment
    except CoinPaymentsProviderError as e:
        context['error'] = e
    return render(request, 'finance/payment_result.html', context)

@csrf_exempt
def ipn_view(request):
    p = request.POST
    ipn_mode = p.get('ipn_mode')
    if ipn_mode != 'hmac':
        return HttpResponseBadRequest('IPN Mode is not HMAC')
    http_hmac = request.META.get('HTTP_HMAC')
    if not http_hmac:
        return HttpResponseBadRequest('No HMAC signature sent.')
    our_hmac = create_ipn_hmac(request)
    print("Our hmac == server hmac - {res}" % {'res': str(our_hmac == http_hmac)})
    merchant_id = getattr(settings, 'COINPAYMENTS_MERCHANT_ID', None)
    if p.get('merchant') != merchant_id:
        return HttpResponseBadRequest('Invalid merchant id')
    tx_id = p.get('txn_id')
    payment = Payment.objects.filter(provider_tx_id__exact=tx_id).first()
    if payment:
        if payment.currency_original != p.get('currency1'):
            return HttpResponseBadRequest('Currency mismatch')
        if payment.status != Payment.PAYMENT_STATUS_PAID:
            # Payments statuses: https://www.coinpayments.net/merchant-tools-ipn
            # Safe statuses: 2 and >= 100
            status = int(p['status'])
            if status == 2 or status >= 100:
                logger.info('Received payment for transaction {} - payment {} ({})'
                            .format(str(tx_id), str(payment.id), str(payment.amount)))
                payment.amount_paid = payment.amount
            else:
                payment.amount_paid = Decimal(p['received_amount'])
            if payment.amount_paid == payment.amount:
                payment.status = Payment.PAYMENT_STATUS_PAID
                payment.save()
                try:
                    T = Transaction.objects.get(transaction_id = txt_id)
                    T.approved = True
                    T.save()
                except Transaction.DoesNotExist:
                    pass
                try:
                    D = Deposit.objects.get(transaction_id = txt_id)
                    D.status = True
                    D.save()
                    p = Profile.objects.get(user=D.user)
                    if D.currency == Bitcoin:
                        p.bitcoin += D.amount
                        p.save()
                    if D.currency == Ethereum:
                        p.ethereum += amount
                        p.save()
                except Deposit.DoesNotExist:
                    pass
                try:
                    D_H = D_History.objects.get(transaction_id = txt_id)
                    D_H.status = True
                    D_H.save()
                except D_History.DoesNotExist:
                    pass
                pass
