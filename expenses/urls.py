from django.urls import path
from . import views

urlpatterns = [
    path('new-expenses/', views.add_new_expenses, name='new_expenses'),
    path('my-expenses/', views.my_expenses, name='my_expenses')
]