from django.urls import path
from . import views


urlpatterns = [
    path('my-categories/', views.my_categories, name="categories")
]