from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers


from store.serializers import UserSerializer,ProductSerializer,BasketItemSerializer,BasketSerializer
from store.models import Product,BasketItem

class SignupView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class ProductsView(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    #url:http://127.0.0.1:8000/api/products/{id}/add_to_basket/
    @action(methods=["post"],detail=True)
    def add_to_basket(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)
        basket_obj=request.user.cart

        basket_products=request.user.cart.cartitem.all().values_list("product",flat=True)
        print(basket_products)
        if int(id) in basket_products:
            basket_item_object=BasketItem.objects.get(basket=basket_obj,product__id=id)
            basket_item_object.quantity=basket_item_object.quantity+int(request.data.get("quantity",1))
            basket_item_object.save()
            serializer=BasketItemSerializer(basket_item_object)
            return Response(data=serializer.data)

        serializer=BasketItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(basket=basket_obj,product=product_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
class BasketView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=request.user.cart
        serializer=BasketSerializer(qs)
        return Response (serializer.data)
    
class BasketItemsView(viewsets.ModelViewSet):
    serializer_class=BasketItemSerializer
    queryset=BasketItem.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def list(self,request,*args,**kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def perform_update(self, serializer):
        user=self.request.user
        owner=self.get_object().basket.owner
        if user==owner:
            return super().perform_update(serializer)
        else:
            raise serializers.ValidationError("owner permission required")
        
    def perform_destroy(self, instance):
        user=self.request.user
        owner=self.get_object().basket.owner
        if user==owner:
            return super().perform_destroy(instance)
        else:
            raise serializers.ValidationError("owner permission required")