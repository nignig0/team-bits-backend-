from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),

    path('business/create/', views.create_business),
    path('business/', views.get_businesses),
    path('business/<int:pk>/', views.get_business_details),

    path('items/create/', views.create_items),
    path('items/', views.get_all_items),
    path('items/<int:pk>/', views.get_item_detail),

    path('cart/', views.get_cart),
    path('cart/add/', views.add_to_cart), 
    path('cart/remove/<int:pk>/', views.remove_from_cart), 
    path('cart/checkout/', views.checkout), 

    path('orders/', views.get_orders),
    path('orders/mark/<int:pk>/', views.mark_order_as_fulfilled_or_not), 

    path('categories/', views.get_categories)
]
