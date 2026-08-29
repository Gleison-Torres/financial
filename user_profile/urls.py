from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit-password/', views.edit_password, name='edit_password')
]