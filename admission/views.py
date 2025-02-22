from django.shortcuts import render
from .models import Orders

# Create your views here.
def list_orders(request):
    context = {
        'orders': Orders.objects.all().using('admission_db')
    }
    return render(request, 'admission/index.html', context)