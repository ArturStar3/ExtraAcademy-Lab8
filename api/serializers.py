from rest_framework import serializers
from .models import Products, Category, Order
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.password_validation import validate_password

User=get_user_model()

class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'quantity', 'category_name']

class AccountCreateSerilizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields = ['username', 'name', 'surname', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password":"Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            name = validated_data['name'],
            surname = validated_data['surname']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'products']

class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class UserOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'orders']
