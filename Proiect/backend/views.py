from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.forms import StickerForm, CustomerForm, CartForm, CartStickerForm
from backend.models import *
from backend.serializers import StickerSerializer, CartSerializer


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
        return Response({'sticker': sticker})

class StickerUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'sticker_update.html'

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

    stickers = Sticker.objects.all()
    context = {'stickers': stickers}
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


@login_required(login_url='login')
def add_to_cart(request, pk):
    sticker = Sticker.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_sticker, sticker_created = CartSticker.objects.get_or_create(cart=cart, sticker=sticker)

    if not sticker_created:
        cart_sticker.quantity += 1
        cart_sticker.save()

    return redirect('store')

@login_required(login_url='login')
def remove_from_cart(request, pk):
    sticker = Sticker.objects.get(pk=pk)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_sticker = cart.cartsticker_set.get(sticker=sticker)
        if cart_sticker.quantity >= 1:
            cart_sticker.delete()
    except CartSticker.DoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    cart_stickers = CartSticker.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_stickers': cart_stickers})

@login_required(login_url='login')
def increase_cart_item(request, pk):
    sticker = Sticker.objects.get(pk=pk)
    cart = request.user.cart
    cart_sticker, created = CartSticker.objects.get_or_create(cart=cart, sticker=sticker)

    cart_sticker.quantity += 1
    cart_sticker.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_cart_item(request, pk):
    sticker = Sticker.objects.get(pk=pk)
    cart = request.user.cart
    cart_sticker = cart.cartsticker_set.get(sticker=sticker)

    if cart_sticker.quantity > 1:
        cart_sticker.quantity -= 1
        cart_sticker.save()
    else:
        cart_sticker.delete()

    return redirect('cart')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartSticker.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_stickers = CartSticker.objects.filter(cart=request.user.cart)
        cart_count = cart_stickers.count()
    else:
        cart_count = 0
    return cart_count

class CreateCart(APIView):
    def get(self, request):
        context = {}
        form = CartForm(request.POST, request.FILES)
        context['form'] = form
        return render(request, "cart_create.html", context)
    def post(self, request):
        form = CartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cart_list')

class CartList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart_list.html'
    def get(self, request):
        queryset = Cart.objects.all()
        return Response({'carts': queryset})

class CartUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart_update.html'

    def get(self, request, pk):
        cart = get_object_or_404(Cart, id=pk)
        serializer = CartSerializer(cart)
        return Response({'serializer': serializer, 'cart': cart})

    def post(self, request, pk):
        cart = get_object_or_404(Cart, id=pk)
        serializer = CartSerializer(cart, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'cart': cart})
        serializer.save()
        return redirect('cart_list')

class CartDelete(APIView):
    def get(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        return render(request, "cart_delete.html", {'cart': cart})
    def post(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        cart.delete()

        return redirect('cart_list')

class CreateCartSticker(APIView):
    def get(self, request):
        context = {}
        form = CartStickerForm(request.POST, request.FILES)
        context['form'] = form
        return render(request, "cartSticker_create.html", context)
    def post(self, request):
        form = CartStickerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cartSticker_list')

class CartStickerList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cartSticker_list.html'
    def get(self, request):
        queryset = CartSticker.objects.all()
        return Response({'cartStickers': queryset})

class CartStickerUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cartSticker_update.html'

    def get(self, request, pk):
        cartSticker = get_object_or_404(CartSticker, id=pk)
        serializer = CartStickerSerializer(cartSticker)
        return Response({'serializer': serializer, 'cartSticker': cartSticker})

    def post(self, request, pk):
        cartSticker = get_object_or_404(CartSticker, id=pk)
        serializer = CartStickerSerializer(cartSticker, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'cartSticker': cartSticker})
        serializer.save()
        return redirect('cartSticker_list')

class CartStickerDelete(APIView):
    def get(self, request, pk):
        cartSticker = get_object_or_404(CartSticker, pk=pk)
        return render(request, "cartSticker_delete.html", {'cartSticker': cartSticker})
    def post(self, request, pk):
        cartSticker = get_object_or_404(CartSticker, pk=pk)
        cartSticker.delete()

        return redirect('cartSticker_list')



