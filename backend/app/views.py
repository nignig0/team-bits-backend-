from datetime import datetime, timedelta
from functools import total_ordering
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from dotenv import load_dotenv
from django.db.models import Q

load_dotenv()


from .serializers import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(secure=True)

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({
            'error': 'Please enter your username and password', 
            'status': status.HTTP_400_BAD_REQUEST
        })
    
    user = authenticate(username= username, password= password)

    if not user:
        return Response({
            'error': 'This user does not exist', 
            'status': status.HTTP_404_NOT_FOUND
        })


    token = Token.objects.get_or_create(user= user)
    serializedUser = UserSerializer(user)
    print(token)
    return Response({
        'token': token[0].key, 
        'message': 'Log in successful!', 
        'user': serializedUser.data  
        
    })


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def register(request):
    try:
        registered_user = RegistrationSerializer(data = request.data)
        if registered_user.is_valid():
            instance = registered_user.create(registered_user.validated_data)
            instance.set_password(request.data.get('password'))
            instance.save()
            #log in the user
            user = authenticate(username = request.data.get('username'), password = request.data.get('password'))
            if not user:
                return Response({
                'error': 'This user does not exist', 
                'status': status.HTTP_404_NOT_FOUND
            })


            token = Token.objects.get_or_create(user= user)
            serializedUser = UserSerializer(user)
            print(token)

            #create Cart
            Cart.objects.create(
                user = user, 
                total = 0
            )
            return Response({
                'token': token[0].key, 
                'message': 'Log in successful!', 
                'user': serializedUser.data  
        
            })
        else:
            return Response(registered_user.errors, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

            

    except Exception as e:
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['POST'])
def create_business(request):
    try:
        business_instance = BusinessSerializer(data = request.data)
        if business_instance.is_valid():
            file = request.FILES['logo']
            name = request.data.get('name')
            cloudinary.uploader.upload(file, public_id = f'logo for business {name}', overwrite = True, uniqueFilename = True)
            url = cloudinary.CloudinaryImage(f'logo for business {name}').build_url()

            business = Business.objects.create(
                name = request.data.get('name'), 
                description = request.data.get('description'),
                owner = request.user, 
                logo_url = url #replace with the cloudinary implementation 
            )
            serialized_business = BusinessSerializer(business)
            return Response({
                'message': 'business created successfully!',
                'data': serialized_business.data
            })
        else:
            return Response(business_instance.errors, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_businesses(request):
    try:
        businesses = Business.objects.all()
        serialized_businesses = BusinessSerializer(businesses, many=True)
        return Response({
            'message': 'Businesses retrieved successfully', 
            'data': serialized_businesses.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_business_details(request, pk):
    try:
        business = Business.objects.get(pk = pk)
        business_items = business.item_set.all()
        serialized_business = BusinessSerializer(business)
        serialized_items = ItemSerializer(business_items, many = True)

        return Response({
            'message': 'Retrieved Business detail successfully!', 
            'business_data': serialized_business.data, 
            'business_items': serialized_items.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })        

@api_view(['POST'])
def create_items(request):
    try:
        instance = ItemSerializer(data = request.data)
        if instance.is_valid():
            business = Business.objects.get(owner = request.user)
            file = request.FILES['picture']
            name = request.data.get('name')
            cloudinary.uploader.upload(file, public_id = f'picture for item {name} for business {business}', overwrite = True, uniqueFilename = True)
            url = cloudinary.CloudinaryImage(f'picture for business {name} for business {business}').build_url()
            category = Category.objects.get(name = request.data.get('category'))
            item  = Item.objects.create(
                name = request.data.get('name'), 
                picture_url = url, 
                business = business, 
                price = int(request.data.get('price')), 
                description = request.data.get('description'), 
                category = category,
            )

            serialized_item = ItemSerializer(item)
            return Response({
                'message': 'item added successfully', 
                'data': serialized_item.data
            })
        else: 
            return Response(instance.errors, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_items(request):
    try:
        items = Item.objects.all()
        serialized_items = ItemSerializer(items, many = True)
        return Response({
            'message': 'Got items successfully',
            'data': serialized_items.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_item_detail(request, pk):
    try:
        item = Item.objects.get(pk = pk)
        serialized_item = ItemSerializer(item)
        return Response({
            'message': 'Got item successfully',
            'data': serialized_item.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['POST'])
def add_to_cart(request): 
    try:
        pk = request.data.get('pk')
        cart = Cart.objects.get(user = request.user)
        item = Item.objects.get(pk = pk)
        order = Order.objects.create(
            item = item, 
            user_from = request.user, 
            amount = int(request.data.get('amount'))
        )
        
        cart.orders.add(order)
        total = int(item.price * order.amount)
        cart.total += total
        cart.save()
        serialized_orders = OrderSerializer(cart.orders, many = True)
        return Response({
            'message': 'Item added to cart successfully!', 
            'cart': serialized_orders.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })


@api_view(['POST'])
def remove_from_cart(request, pk): #primary key of order to be removed 
    try:
        cart = Cart.objects.get(user = request.user)
        order  = Order.objects.get(pk = pk)
        cart.orders.remove(order)

        total = int(order.amount * order.item.price)
        cart.total -= total
        cart.save()
        serialized_orders = OrderSerializer(cart.orders, many = True)
        return Response({
            'message': 'Item added to cart successfully!', 
            'cart': serialized_orders.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['POST'])
def checkout(request):
    try:
        cart = Cart.objects.get(user = request.user)
        for order in cart.orders:
            order.active = True
            order.save()

        cart.orders.clear()
        cart.total = 0
        cart.save()
        return Response({
            'message': 'Checked out successfully'
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })         

@api_view(['GET'])
def get_cart(request):
    try:
        cart = Cart.objects.get(user = request.user)
        serialized_cart = CartSerializer(cart)
        return Response({
            'message': 'retrieved cart successfully!', 
            'cart': serialized_cart.data
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })    

@api_view(['GET'])
def get_orders(request):
    try:
        business = Business.objects.get(owner = request.user)
        orders = Order.objects.filter(Q(fulfilled = False) & Q(item__in = business.item_set.all()))
        #get orders that are unfulfilled and relate to the business in question 
        serialized_orders = OrderSerializer(orders, many = True)

        return Response({
            'message': 'Retrieved orders successfully', 
            'orders': serialized_orders.data
        }) 

    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })

@api_view(['POST'])
def mark_order_as_fulfilled_or_not(request, pk):
    try:
        order = Order.objects.get(pk = pk)
        previous_flag = order.fulfilled
        order.fulfilled = not order.fulfilled
        order.save()

        return Response({
            'message': f'Changed {previous_flag} to {order.fulfilled}'
        })
    except Exception as e: 
        print(e)
        return Response({
            "error": True,
            "message": "There was an error"
        })
