from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]
