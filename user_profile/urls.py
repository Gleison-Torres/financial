from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email_change, name='confirm_email_change'),
    path('change-password/', views.change_password, name='change_password')
]