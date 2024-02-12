from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products_set')
    date = models.DateTimeField(auto_now_add=True)

