from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from JustDoIT.backends import authenticate
from authentication.models import UserCreateCode, ActivityCategory

User = get_user_model()


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = ('id', 'description')


class UserCreateSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'image', 'CV', 'activities', 'activities_info')
        extra_kwargs = {'activities': {'required': False, 'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    activities_info = ActivitySerializer(many=True, read_only=True, source='activities')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'firstname', 'groups',
                  'lastname', 'photo', 'sex', 'region', 'doc_type', 'doc_info',
                  'is_entity', 'activity', 'image', 'CV', 'activities_info', 'last_seen')


class UpdatePasswordSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        data = self.initial_data
        user = data.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get_by_natural_key(user)
        except User.DoesNotExist:
            raise ValidationError('Пользователь под данным номером не обнаружен')
        return user


class CodeSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=True):
        data = self.initial_data
        user = data.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get_by_natural_key(user)
            code = UserCreateCode.objects.get(user=user)
            assert code.code == data.get('code')
        except User.DoesNotExist:
            raise ValidationError('Пользователь под данным номером не обнаружен')
        except UserCreateCode.DoesNotExist:
            raise ValidationError('Невозможно подтвердить код')
        except AssertionError:
            raise ValidationError('Неверный код')
        if hasattr(self, 'update_passwd'):
            try:
                assert data.get('password')
            except AssertionError:
                raise ValidationError('Вы не ввели пароль')
            code.delete()
            if not user.is_active:
                raise ValidationError('Пользователь не активен для восстановления пароля')
            user.set_password(data.get("password"))
            user.save()
        else:
            code.delete()
            user.is_active = True
            user.save()
        return user

    class Meta:
        model = UserCreateCode


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        self.user = authenticate(attrs[self.username_field], attrs["password"])

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

