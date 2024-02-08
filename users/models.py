from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.services import function_valid_until

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=100, verbose_name='имя пользователя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия пользователя')
    email = models.EmailField(unique=True, verbose_name='адрес электронной почты')
    image = models.ImageField(upload_to='users/', default='users/avatar_default.jpeg', verbose_name='аватар',
                              **NULLABLE)
    referral_code_refer = models.CharField(max_length=15, **NULLABLE)
    refer = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name}, {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Code(models.Model):

    referral_code = models.CharField(max_length=15, unique=True, **NULLABLE)
    valid_until = models.DateField(default=function_valid_until, **NULLABLE)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                                 verbose_name='создатель')

    def __str__(self):
        return f'{self.referral_code} ({self.owner})'

    class Meta:
        verbose_name = 'реферальный код'
        verbose_name_plural = 'реферальные кода'
