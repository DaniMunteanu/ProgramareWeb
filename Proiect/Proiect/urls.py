"""Proiect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from backend.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('sticker_create/', CreateSticker.as_view(), name='sticker_create'),
    path('sticker_list/', StickerList.as_view(), name='sticker_list'),
    path('sticker_update/<int:pk>', StickerUpdate.as_view(), name='sticker_update'),
    path('sticker_detail/<int:pk>', StickerDetail.as_view(), name='sticker_detail'),
    path('sticker_delete/<int:pk>', StickerDelete.as_view(), name='sticker_delete'),
    path('', store_view, name='store'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/',logout_user, name='logout'),
    path('user_list/', UserList.as_view(), name='user_list'),
    path('user_delete/<int:pk>', UserDelete.as_view(), name='user_delete'),

    path('checkout/', checkout_view, name='checkout'),

    path('cart_create/', CreateCart.as_view(), name='cart_create'),
    path('cart_list/', CartList.as_view(), name='cart_list'),
    path('cart_update/<int:pk>', CartUpdate.as_view(), name='cart_update'),
    path('cart_delete/<int:pk>', CartDelete.as_view(), name='cart_delete'),

    path('cartSticker_create/', CreateCartSticker.as_view(), name='cartSticker_create'),
    path('cartSticker_list/', CartStickerList.as_view(), name='cartSticker_list'),
    path('cartSticker_update/<int:pk>', CartStickerUpdate.as_view(), name='cartSticker_update'),
    path('cartSticker_delete/<int:pk>', CartStickerDelete.as_view(), name='cartSticker_delete'),

    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', view_cart, name='cart'),
    path('increase-cart-item/<int:pk>/', increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:pk>/', decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', fetch_cart_count, name='fetch-cart-count'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
