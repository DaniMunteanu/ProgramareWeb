from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
import json
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.forms import StickerForm, CustomerForm
from backend.models import *
from backend.serializers import StickerSerializer

# Create your views here.

class CreateSticker(APIView):
    def get(self, request):
        context = {}
        form = StickerForm(request.POST, request.FILES)
        context['form'] = form
        return render(request, "sticker_create.html", context)
    def post(self, request):
        form = StickerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('sticker_list')

class StickerList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sticker_list.html'
    def get(self, request):
        queryset = Sticker.objects.all()
        return Response({'stickers': queryset})

class StickerDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sticker_detail.html'

    def get(self, request, pk):
        sticker = get_object_or_404(Sticker, id=pk)
        serializer = StickerSerializer(sticker)
        return Response({'serializer': serializer, 'sticker': sticker})

    def post(self, request, pk):
        sticker = get_object_or_404(Sticker, id=pk)
        serializer = StickerSerializer(sticker, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'sticker': sticker})
        serializer.save()
        return redirect('sticker_list')

class StickerDelete(APIView):
    def get(self, request, pk):
        sticker = get_object_or_404(Sticker, pk=pk)
        return render(request, "sticker_delete.html", {'sticker': sticker})
    def post(self, request, pk):
        sticker = get_object_or_404(Sticker, pk=pk)
        sticker.delete()
        return redirect('sticker_list')

def register(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered!"))
            return redirect('store')
        else:
            messages.success(request, ("There was an error during registration!"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

class UserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_list.html'
    def get(self, request):
        queryset = User.objects.all()
        return Response({'users': queryset})

class UserDelete(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, "user_delete.html", {'user': user})
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('store')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('store')

def store_view(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        stickers = order.ordersticker_set.all()
        cartStickers = order.get_cart_stickers
    else:
        stickers = []
        order = {'get_cart_total': 0, 'get_cart_stickers': 0}
        cartStickers = order['get_cart_items']


    stickers = Sticker.objects.all()
    context = {'stickers': stickers, 'cartStickers': cartStickers}
    return render(request, "store.html", context)

def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        stickers = order.ordersticker_set.all()
        cartStickers = order.get_cart_stickers
    else:
        stickers = []
        order = {'get_cart_total': 0, 'get_cart_stickers': 0}
        cartStickers = order['get_cart_items']

    context = {'stickers': stickers, 'order': order}
    return render(request, "cart.html", context)

def checkout_view(request):
    '''
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
    '''


    context = {}
    return render(request, "checkout.html", context)

def update_cart(request):
    data = json.loads(request.body)
    stickerId = data['stickerId']
    action = data['action']
    print('Action:', action)
    print('Sticker:', stickerId)

    customer = request.user
    sticker = Sticker.objects.get(id=stickerId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)
    orderSticker, created = Order.objects.get_or_create(order=order, sticker=sticker)

    if action == 'add':
        orderSticker.quantity = (orderSticker.quantity + 1)
    elif action == 'remove':
        orderSticker.quantity = (orderSticker.quantity - 1)

    orderSticker.save()

    if orderSticker.quantity <= 0:
        orderSticker.delete()

    return JsonResponse('Sticker was added', safe=False)


