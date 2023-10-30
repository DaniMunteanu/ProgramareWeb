from django.shortcuts import render

from backend.models import *

# Create your views here.

def store_view(request):
    stickers = Sticker.objects.all()
    context = {'stickers': stickers}
    return render(request, "store.html", context)

def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items}
    return render(request, "cart.html", context)

def checkout_view(request):
    context = {}
    return render(request, "checkout.html", context)

def sticker_detail(request):
    context = {}
    return render(request, "cart.html", context)
