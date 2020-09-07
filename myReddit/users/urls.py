from django.urls import path
from django.contrib.auth import views
from .views import register, profile,profile_edit ,email_verification_confirm,email_verification_done

app_name = 'users'

urlpatterns = [
    path('register/',register, name='register'),
    path('login/',views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password-reset/',views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/done/',views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-complete/',views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('email_verification_confirm/<uidb64>/<token>',email_verification_confirm,name='email_verification_confirm'),
    path('email_verification_done/', email_verification_done, name='email_verification_done'),
    path('edit/profile/',profile_edit,name='profile_edit'),
    path('profile/',profile,name='profile'),
]