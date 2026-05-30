from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.index_login, name="login")
]
