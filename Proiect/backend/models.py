from django.db import models
from django.contrib.auth.models import User

from Proiect import settings


# Create your models here.

class Sticker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    length = models.FloatField()
    height = models.FloatField()
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        return url

class CartSticker(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    sticker = models.ForeignKey(Sticker, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.sticker.name}"
    def total(self):
        return self.sticker.price * self.quantity

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stickers = models.ManyToManyField(Sticker, through='CartSticker')

    def __str__(self):
        return f"Cart for {self.user.username}"

