from . models import Products, Category, Order
from django.shortcuts import get_object_or_404
from .  import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.decorators import action

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def list(self, request):
        queryset = Products.objects.filter(quantity__gt=0, is_active=True)
        serializer = serializers.ProductsSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Products, pk=pk, is_active=True)
        serializer = serializers.ProductsSerializer(product)
        return Response(serializer.data)

class AccountViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = serializers.AccountCreateSerilizer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self, *args, **kwargs):
        if self.action=="list":
            return serializers.CategorySerializer
        if self.action=='retrieve':
            return serializers.CategoryWithProductsSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self):
        if self.action=="create":
            return serializers.OrderCreateSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Products, id=serializer.validated_data['product_id'])
            if product:
                user=request.user
                order=Order.objects.create(user=user, product=product)
                return Response({
                    "id": order.id,
                    "user": order.user.name,
                    "product":order.product.name
                })

class UserOrdersViewSet(viewsets.ModelViewSet):

    User = get_user_model()
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def get_serializer_class(self):
        if self.action=='user_orders':
            return serializers.UserOrderSerializer

    @action(detail=True, url_path="orders", methods=("POST",))
    def user_orders (self, request, *args, **kwargs):
        User = get_user_model()
        user = get_object_or_404(User, id=kwargs['pk'])
        serializer = serializers.UserOrderSerializer(user)
        return Response(serializer.data)





    