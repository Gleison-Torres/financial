from django.urls import path
from . import views

urlpatterns = [
    path('new-expenses/', views.add_new_expenses, name='new_expenses')
]