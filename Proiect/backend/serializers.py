from rest_framework import serializers

from backend.models import Sticker, CartSticker, Cart


class StickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sticker
        fields = ['name', 'length', 'height', 'price', 'image']

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user', 'stickers']

class CartStickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartSticker
        fields = ['cart', 'sticker']

