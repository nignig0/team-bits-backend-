from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from .serializers import *

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

