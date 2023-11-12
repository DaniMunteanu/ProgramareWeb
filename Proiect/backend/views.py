from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

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
        sticker = get_object_or_404(Sticker, pk=pk)
        serializer = StickerSerializer(sticker)
        return Response({'serializer': serializer, 'sticker': sticker})

    def post(self, request, pk):
        sticker = get_object_or_404(Sticker, pk=pk)
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

"""
class StickerDetail(APIView):
"""
    #Retrieve, update or delete a snippet instance.
"""
    def get_object(self, pk):
        try:
            return Sticker.objects.get(pk=pk)
        except Sticker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = StickerSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = StickerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
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

