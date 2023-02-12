from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from authentication import utils
from authentication.models import UserCreateCode, ActivityCategory
from authentication.serializers import UserCreateSerializer, MyTokenObtainPairSerializer, CodeSerializer, \
    UpdatePasswordSerializer, ActivitySerializer, ProfileSerializer

User = get_user_model()


@api_view(["post"])
def reset_password(request):
    serializer = UpdatePasswordSerializer(data=request.data)
    user = serializer.is_valid(raise_exception=True)
    utils.gen_code(user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["get"])
def get_categories(request):
    return Response(ActivitySerializer(ActivityCategory.objects.all(), many=True).data)


class UserViewSet(viewsets.ModelViewSet, TokenObtainPairSerializer):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return CodeSerializer
        elif self.action == 'retrieve':
            return ProfileSerializer
        return UserCreateSerializer

    def get_permissions(self):
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utils.gen_code(self.perform_create(serializer))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if request.data.get('update_passwd'):
            serializer.update_passwd = True
        user = serializer.is_valid()
        refresh = self.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return Response(data)

    def perform_create(self, serializer):
        return serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
