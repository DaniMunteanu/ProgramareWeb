from django.contrib import messages
from django.contrib.auth import logout
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
"""
class StickerList(APIView):
"""
   # List all snippets, or create a new snippet.
"""
    def get(self, request, format=None):
        snippets = Sticker.objects.all()
        serializer = StickerSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
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
    if request.POST == 'POST':
        form = CustomerForm()
        if form.is_valid():
            form.save()
            redirect('store')
    else:
        form = CustomerForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login_user(request):
    return render(request, 'login.html', {})
def logout_user(request):
    logout(request)
    messages.succes(request, ("You have been logged out!"))
    return redirect('store')

def store_view(request):
    stickers = Sticker.objects.all()
    context = {'stickers': stickers}
    return render(request, "store.html", context)

def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items}
    return render(request, "cart.html", context)

def checkout_view(request):
    context = {}
    return render(request, "checkout.html", context)

def updateSticker(request):
    return JsonResponse('Sticker was added', safe=False)