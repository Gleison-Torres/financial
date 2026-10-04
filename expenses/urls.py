from django.urls import path
from . import views

urlpatterns = [
    path('new-expenses/', views.add_new_expenses, name='new_expenses'),
    path('my-expenses/', views.my_expenses, name='my_expenses'),
    path('delete-expenses/<int:expense_id>/', views.delete_expenses, name='delete_expenses'),
    path('edit-expenses/', views.edit_expenses, name='edit_expenses')
]