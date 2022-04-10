from accounts import views as accounts_views

from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('my-profile/', accounts_views.MyProfile.as_view(), name='my-profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
