from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from .forms import UserRegistrationForm, ProfileUpdateForm
from .models import Profile
from finance.models import Transaction, Deposit, Payment_Request
from .tasks import send_registration_email_task
# Create your views here.

def registration (request):
    if request.user.is_authenticated:
        return redirect ('dashboard')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                name = f'{first_name} {last_name}'
                email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                country = form.cleaned_data.get('country')
                pin = form.cleaned_data.get('tpin1')
                referral = form.cleaned_data.get('referral')
                profile = Profile.objects.get(user=User.objects.get(username=username))
                send_registration_email_task.delay(name, username, email)
                if referral:
                    try:
                        ref = User.objects.get(username=referral)
                    except User.DoesNotExist:
                        ref = None
                    if ref == None:
                        profile.country=country
                        profile.pin=pin
                        profile.save()
                    else:
                        profile.referral = ref
                        profile.country=country
                        profile.pin=pin
                        profile.save()
                else:
                    profile.country=country
                    profile.pin=pin
                    profile.save()
                messages.success(request, f'Account was created for {username}')
                return redirect ('login')
        else:
            form = UserRegistrationForm()
        context = {'title': 'Register',
                    'form': form}
        return render (request, "account/register.html", context)

def userLogin (request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR Password is incorrect')
        context = {
            'title' : 'Login'
        }
    return render(request, 'account/login.html', context)

def logoutUser (request):
    logout(request)
    return redirect ('login')

@login_required()
def change_password (request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect ('password_change_done')
    else:
        form = PasswordChangeForm(user = request.user)
        context = {
            'form': form
        }
        return render(request, 'account/password_change_form.html', context)

@login_required()
def password_change_done (request):
    return render(request, 'account/password_change_done.html')

@login_required()
def userAccount(request):
    my_account = Deposit.objects.filter(user=request.user.id)
    active_deposits_amount = 0.0
    matured_deposits_amount = 0.0
    interest_today = 0.0
    interest_earnings = 0.0
    earning_today = 0.0
    total_earning = 0.0
    total_payout = 0.0
    pending_payout = 0.0
    referral_interest = 0.0
    for item in my_account:
        interest_today += item.interest_today
        interest_earnings += item.interest_earnings
        earning_today += float(item.amount) + float(item.interest_today)
        total_earning += float(item.amount) + float(item.interest_earnings)
        if item.status:
            active_deposits_amount += float(item.amount)
        if item.matured:
            matured_deposits_amount += float(item.amount)
    for payout in  Payment_Request.objects.filter(user=request.user.id):
        if payout.status:
            total_payout += float(payout.amount)
        else:
            pending_payout += float(payout.amount)
    referral = Profile.objects.filter(referral=request.user.id)
    ref_deposit = Deposit.objects.filter(user=request.user.profile.referral)
    for ref in ref_deposit:
        referral_interest += ref.referral_interest
    context = {
    "title": "Dashboard",
    "transactions": Transaction.objects.filter(user=request.user.id),
    "active_deposits_amount":active_deposits_amount,
    "matured_deposits_amount": matured_deposits_amount,
    "total_payout": total_payout,
    "pending_payout": pending_payout,
    "interest": {
        "interest_today":interest_today,
        "interest_earnings":interest_earnings,
        "earning_today": earning_today,
        "total_earning": total_earning,
        "referral_number": referral.count(),
        "referral_interest": referral_interest,
    },
    }
    return render(request, 'account/my_account.html', context)

@login_required()
def view_profile(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, instance = request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'p_form': p_form
    }
    return render(request, 'account/view_profile.html', context)
