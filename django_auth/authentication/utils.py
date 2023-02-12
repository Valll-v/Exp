import random

from JustDoIT import settings
from authentication.models import UserCreateCode


USE_CODE_AUTH = settings.USE_CODE_AUTH
DEFAULT_CODE = settings.DEFAULT_CODE


def gen_code(user):
    code, _ = UserCreateCode.objects.get_or_create(user=user)
    code.code = send_phone_code(user)
    code.save()


def send_phone_code(user):
    return random.randint(1000, 9999) if USE_CODE_AUTH else DEFAULT_CODE
