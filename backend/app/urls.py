from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register), 
    path('items/', views.get_all_items)
]
