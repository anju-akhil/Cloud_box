from rest_framework import serializers
from django.contrib.auth.models import User

from store.models import Product,BasketItem,Basket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class ProductSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
        model=Product
        fields="__all__"

class BasketItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(read_only=True)
    total=serializers.IntegerField(read_only=True)
    class Meta:
        model=BasketItem
        fields="__all__"
        read_only_fields=["id","basket","product","updated_at","is_active","total"]

class BasketSerializer(serializers.ModelSerializer):
    cart_items=BasketItemSerializer(read_only=True,many=True)
    cart_item_quantity=serializers.CharField(read_only=True)
    sub_total=serializers.IntegerField(read_only=True)
    class Meta:
        model=Basket
        fields=["id"
                ,"owner","created_at","updated_at","is_active","cart_items","cart_item_quantity","sub_total"]