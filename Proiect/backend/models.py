from django.db import models
from django.contrib.auth.models import User

from Proiect import settings


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    def __str__(self):
        return self.name
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

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    order_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    sticker = models.ForeignKey(Sticker, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
