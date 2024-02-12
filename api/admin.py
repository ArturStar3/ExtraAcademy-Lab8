from django.contrib import admin
from .models import Category, Products, Order

admin.site.register(Category)
admin.site.register(Order)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
