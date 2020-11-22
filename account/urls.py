from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.userLogin, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("dashboard/", views.userAccount, name="dashboard"),
    path("dashboard/profile/", views.view_profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("password-change-done/", views.password_change_done, name="password_change_done"),
    path("password-reset/",
    auth_views.PasswordResetView.as_view(template_name = 'account/password_reset.html'),
    name="password_reset"),
    path("password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
    name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/done/",
    auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html'),
    name="password_reset_complete"),
]
