from django.shortcuts import render
from .models import Orders

def list_orders(request):
    context = {
        'orders': Orders.objects.all()
    }
    return render(request, 'admission/index.html', context)