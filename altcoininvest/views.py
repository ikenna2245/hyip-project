from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Blog, Comment, Support, Subscriber, FAQ, Ads
from account.models import Top_investor, Testimonial, AdminFact
from finance.models import Deposit, Payment_Request, D_History

# Create your views here.
def index (request):
    if request.method == 'POST':
        email = request.POST.get("email")
        s = Subscriber(email=email)
        s.save()
        return redirect('home')
    context = {
        'top_investors':Top_investor.objects.all(),
        'testimonials':Testimonial.objects.all(),
        'deposits': D_History.objects.order_by('-date')[:7],
        'withdraws': Payment_Request.objects.order_by('-date')[:7],
        'blogs': Blog.objects.all()[:3],
        'fact': AdminFact.objects.first(),
        'ads': Ads.objects.all(),
    }
    return render(request, 'altcoininvest/index.html', context)

def about (request):
    context = {
    'title': 'About Us',
    'top_investors':Top_investor.objects.all(),
    'testimonials':Testimonial.objects.all(),
    'fact': AdminFact.objects.first()
    }
    return render(request, 'altcoininvest/about_us.html', context)

def contactPage (request):
    context = {
    "title": "Contact Us",
    'fact': AdminFact.objects.first()
    }
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        support = Support(first_name=fname, last_name=lname, subject=subject, email=email, message=message)
        support.save()
        messages.success(request, 'Contact Form: Message has been sent')
        return render(request, 'altcoininvest/contact_us.html',context)
    return render(request, 'altcoininvest/contact_us.html',context)

def faq (request):
    if request.method == 'POST':
        fullName = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        support = Support(first_name = fullName, last_name = fullName, subject = subject, message = message, email = email)
        support.save()
        messages.success(request, "Your request has been submitted")
        return redirect ('faq')
    context = {
    "title": "FAQ",
    'fact': AdminFact.objects.first(),
    'faqs': FAQ.objects.all()
    }
    return render(request, 'altcoininvest/faq.html', context)

def blog (request):
    context = {
    "title": "Blog - Home",
    "blogs": Blog.objects.all(),
    'fact': AdminFact.objects.first()
    }
    return render(request, 'altcoininvest/blog_category.html', context)

def blog_single(request, pk):
    blog = Blog.objects.get(pk=pk)
    context = {
    "title": blog.title,
    "blog": blog,
    "blogs": Blog.objects.all(),
    "comments": Comment.objects.filter(approve=True, category = blog.title),
    'fact': AdminFact.objects.first()
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        category = request.POST.get('category')
        new_comment = Comment(name=name, email=email, comment=message, category=category)
        new_comment.save()
        messages.success(request, 'Comment Submitted')
        return render(request, 'altcoininvest/blog_single.html', context)
    return render(request, 'altcoininvest/blog_single.html', context)

def investment (request):
    context = {
    "title": "Investment Plan",
    'deposits': Deposit.objects.order_by('-date'),
    'withdraws': Payment_Request.objects.order_by('-date'),
    'fact': AdminFact.objects.first()
    }
    return render(request, 'altcoininvest/investment.html', context)
