from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    
    class Meta: 
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

        def create(self, validated_data):
            user = User.objects.create(
                username = validated_data['username'], 
                email = validated_data['email'],
                first_name = validated_data['first_name'], 
                last_name = validated_data['last_name']
            )

            return user



class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'pk']
        read_only_fields = ['pk', 'username']

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['pk','name', 'description','owner', 'logo_url']
        read_only_fields = ['pk','owner','logo_url', ]

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    class Meta: 
        model = Item
        fields = ['name', 'price', 'description', 'category', 'business', 'picture_url']
        read_only_fields = ['business', 'picture_url']

class OrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Order
        fields = ['item', 'amount', 'user_from',]
        read_only_fields = ['user_from', 'amount'] 

class CartSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cart
        fieds = ['orders', 'total']
        read_only_fields = ['orders', 'total']
