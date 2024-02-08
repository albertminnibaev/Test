import random

from rest_framework import serializers

from users.models import User, Code
from users.validators import EmailValidators


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        validators = [
            EmailValidators(fields=('email',)),
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        # user.referral_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        user.save()
        return user


class UserReferralRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'referral_code_refer']
        validators = [
            EmailValidators(fields=('email',)),
        ]

    def create(self, validated_data):
        referral_code_refer = validated_data['referral_code_refer']
        user_refer = Code.objects.get(referral_code=referral_code_refer).owner
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.refer = user_refer
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserReferralSerializer(serializers.ModelSerializer):
    referral = UserSerializer(source='user_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['referral']


class CodeCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        code = Code.objects.create(**validated_data)
        code.referral_code = ''.join([str(random.randint(0, 9)) for _ in range(14)])
        code.save()
        return code

    class Meta:
        model = Code
        fields = []
#
#
# class CodeRetrieveSerializer(serializers.ModelSerializer):
#
#     email = serializers.EmailField()
#
#     def get_referral_code(self, value):
#         email = self.context['request'].get('email')
#         user = get_object_or_404(User, email=email)
#         referral_code = user.referral_code
#         return referral_code
#
#     class Meta:
#         model = User
#         fields = '__all__'
