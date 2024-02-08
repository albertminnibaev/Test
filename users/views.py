import random

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from config import settings
from users.models import User, Code
from users.permissions import IsProfileUser
from users.serializers import UserSerializer, UserRegisterSerializer, CodeCreateSerializer, \
    UserReferralRegisterSerializer, UserReferralSerializer


# регистрация пользователя
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


# регистрация пользователя как как реферала
class UserReferralRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserReferralRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileUser]


# получение информации о рефералах по id реферера
class UserReferralRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserReferralSerializer
    queryset = User.objects.all()


# создание реферального кода
class CodeCreateAPIView(generics.CreateAPIView):
    serializer_class = CodeCreateSerializer
    queryset = Code.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_code = serializer.save()
        new_code.owner = self.request.user
        new_code.referral_code = ''.join([str(random.randint(0, 9)) for _ in range(14)])
        new_code.save()


# удаление реферального кода
class CodeDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        code = get_object_or_404(Code, owner=user)
        if settings.CACHE_ENABLED:
            referral_code = cache.get(code.id)
            if referral_code:
                cache.delete(code.id)
        code.delete()
        return Response({'message': 'referral_code delete'}, status=status.HTTP_204_NO_CONTENT)


# получения реферального кода по email адресу рефера
class CodeRetrieveAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = request.data
        email = data.get('email')

        if not email:
            return Response({'error': 'email are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)

        if not user:
            return Response({'error': 'the user with this address is not registered'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            Code.objects.get(owner=user.id)
        except Exception:
            return Response({'error': 'the user with this address does not have a registered referral key'},
                            status=status.HTTP_400_BAD_REQUEST)
        if settings.CACHE_ENABLED:
            key = Code.objects.get(owner=user.id).id
            referral_code = cache.get(key)
            if referral_code is None:
                referral_code = Code.objects.get(owner=user.id).referral_code
                cache.set(key, referral_code)
        else:
            referral_code = Code.objects.get(owner=user.id).referral_code
        return Response({'referral_code': referral_code}, status=status.HTTP_200_OK)
