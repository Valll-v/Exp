from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


def authenticate(phone_number=None, password=None):
    try:
        user = User.objects.get(
            Q(phone_number=phone_number) | Q(email=phone_number)
        )

    except User.DoesNotExist:
        return None

    if user and check_password(password, user.password):
        return user

    return None
