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
    path('sticker_list/', StickerList.as_view(), name='sticker_list'),
    path('stickers/<int:pk>', StickerDetail.as_view(), name='sticker_detail'),
    path('sticker_delete/<int:pk>', StickerDelete.as_view(), name='sticker_delete'),
    path('stickers/', StickerDetail.as_view()),
    path('', store_view, name='store'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
