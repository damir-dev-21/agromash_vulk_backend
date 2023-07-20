from django.shortcuts import render
from .serializers import UserSerializer, OrderSerializer, ProducerSerializer, CarSerializer
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Item, Car, Order, Mark, Producer
from django.forms.models import model_to_dict
import jwt
import datetime
import json

import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO


class ItemViews(APIView):

    def post(self, request):

        item = Item.objects.filter(name=request.data['item']).first()
        marks = item.marks.all()
        pass


class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        responce = Response()
        responce.data = {
            'message': 'success',
            'data': serializer.data
        }
        return responce


class AllBrands(APIView):

    def get(self, request):

        producers = Producer.objects.filter().all()

        producersSerializers = ProducerSerializer(data=producers, many=True)
        producersSerializers.is_valid()
        responce = Response()
        responce.data = {
            'brands': producersSerializers.data
        }

        return responce


def create_image_from_base64(base64_string):
    # Декодируем base64 строку
    decoded_image = base64.b64decode(base64_string)

    # Создаем объект Image из декодированных данных
    image = Image.open(BytesIO(decoded_image))

    # Может потребоваться изменить размер или выполнить другую обработку изображения здесь,
    # в зависимости от ваших требований

    # Получаем тип изображения
    image_format = image.format.lower()

    # Создаем временный объект InMemoryUploadedFile
    image_io = BytesIO()
    image.save(image_io, format=image_format)
    image_file = InMemoryUploadedFile(
        image_io, None, "image.png", f'images/{image_format}', len(
            image_io.getvalue()), None
    )

    return image_file


class CreateOrder(APIView):

    def post(self, request):

        responce = Response()

        try:
            carBody = request.data['car']
            brandBody = request.data['brand']
            userBody = request.data['user']
            marksBody = request.data['marks']

            newCar = Car()
            newCar.number = carBody['number']
            newCar.image = create_image_from_base64(carBody['base64_file'])
            newCar.save()

            brand = Producer.objects.filter(name=brandBody).first()
            user = User.objects.filter(id=userBody['id']).first()

            newOrder = Order()
            newOrder.carNumber = newCar
            newOrder.brand = brand
            newOrder.user = user
            newOrder.save()

            idOrder = newOrder.id

            for item in marksBody:
                image_field = create_image_from_base64(item['base64_file'])

                newMark = Mark()
                newMark.mark = item['mark']
                newMark.photo = image_field
                newMark.order = newOrder
                newMark.save()

            responce.data = {
                'status': True,
                'message': 'OK'
            }

            return responce
        except Exception as e:
            responce.data = {
                'status': False,
                'message':e 
            }
        
        return responce


class CheckCar(APIView):

    def post(self, request):

        number = request.data['number']
        imageBase64 = request.data['base64_file']
        image_field = create_image_from_base64(imageBase64)

        car = Car.objects.filter(number=number).first()

        if car is None:
            responce = Response()

            responce.data = {
                'status': True,
                'message': 'OK'
            }

            return responce
        else:
            responce = Response()

            responce.data = {
                'status': False,
                'message': 'Такая машина уже есть!'
            }

            return responce


class CheckAccessView(APIView):

    def post(self, request):

        name = request.data['name']
        password = request.data['password']

        user = User.objects.filter(name=name).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        if user.district == "" or user.latitude == "" or user.longitude == "":
            responce = Response()

            responce.data = {
                'status': False,
            }

            return responce
        else:
            serializer = UserSerializer(user)

            orders = Order.objects.filter(user=user).all()

            responce = Response()

            responce.set_cookie(key='jwt', value=token, httponly=True)

            responce.headers = {
                'jwt': token,
            }
            orderSerializer = OrderSerializer(orders, many=True)
            responce.data = {
                'status': True,
                'jwt': token,
                'user': serializer.data,
                'orders': orderSerializer.data
            }

            return responce


class LoginView(APIView):

    def post(self, request):

        # a = Item.objects.first().marks.all()
        # for item in a:
        #     print(item.mark)

        name = request.data['name']
        password = request.data['password']
        lat = request.data['latitude']
        lon = request.data['longitude']
        district = request.data['district']
        fio = request.data['fio']

        user = User.objects.filter(name=name).first()

        user.latitude = lat
        user.longitude = lon
        user.district = district
        user.fio = fio

        user.save()

        if user is None:
            raise AuthenticationFailed('User not found')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        serializer = UserSerializer(user)
        responce = Response()

        orders = Order.objects.filter(user=user).all()
        orderSerializer = OrderSerializer(orders, many=True)

        responce.set_cookie(key='jwt', value=token, httponly=True)

        responce.headers = {
            'jwt': token,
        }

        responce.data = {
            'status': True,
            'jwt': token,
            'user': serializer.data,
            'orders': orderSerializer.data
        }

        return responce


class LogoutView(APIView):

    def post(self, request):
        responce = Response()
        responce.delete_cookie('jwt')
        responce.data = {
            'status': True
        }
        return responce
