from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (UserListAPIView, UserUpdateAPIView, UserRetrieveAPIView, UserRegisterAPIView,
                         CodeCreateAPIView, CodeDestroyAPIView, CodeRetrieveAPIView, UserReferralRegisterAPIView,
                         UserReferralRetrieveAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('user/', UserListAPIView.as_view(), name='user_list'),
    path('user/register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('user/register_referral/', UserReferralRegisterAPIView.as_view(), name='register_referral'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_get'),
    path('user/referral/<int:pk>/', UserReferralRetrieveAPIView.as_view(), name='referral'),
    path('code/create/', CodeCreateAPIView.as_view(), name='create_code'),
    path('code/delete/', CodeDestroyAPIView.as_view(), name='code_delete'),
    path('code/referral_code/', CodeRetrieveAPIView.as_view(), name='referral_code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
