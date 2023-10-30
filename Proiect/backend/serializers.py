from rest_framework import serializers

from backend.models import Sticker

class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['lungime', 'inaltime', 'pret', 'imagine']