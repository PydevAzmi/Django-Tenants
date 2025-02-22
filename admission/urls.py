from django.urls import path

from admission.views import list_orders

urlpatterns = [
    path('orders/', list_orders, name='list_orders'),
]