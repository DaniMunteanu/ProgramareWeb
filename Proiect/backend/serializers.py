from rest_framework import serializers

from backend.models import Sticker

#class StickerSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = Sticker
   #     fields = ['name', 'length', 'height', 'price', 'image']

class StickerSerializer(serializers.ModelSerializer):
    '''
    name = serializers.CharField(max_length=200)
    length = serializers.FloatField()
    height = serializers.FloatField()
    price = serializers.FloatField()
    image = serializers.ImageField()

    def create(self, validated_data):
        return Sticker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.length = validated_data.get('length', instance.length)
        instance.height = validated_data.get('height', instance.height)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    '''
    class Meta:
        model = Sticker
        fields = ['name', 'length', 'height', 'price', 'image']
