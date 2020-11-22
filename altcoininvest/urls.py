from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about-us/", views.about, name="about_us"),
    path("contact-us/", views.contactPage, name="contact_us"),
    path("faq/", views.faq, name="faq"),
    path("blog/category/", views.blog, name="blog"),
    path("blog/<int:pk>/", views.blog_single, name="blog_single"),
    path("investment/", views.investment, name="investment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
