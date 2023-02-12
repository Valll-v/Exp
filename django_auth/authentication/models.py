from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.contrib.auth.models import PermissionsMixin, UserManager, Group
from django.core.validators import validate_email
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        print("aboba")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def _create_user(self, phone_number, email, password, **extra_fields):
        groups = extra_fields.pop('groups', [])
        activities = extra_fields.pop('activities', [])
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        user.groups.set(groups)
        user.activities.set(activities)
        return user

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, email, password, **extra_fields)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Docs(models.TextChoices):
        PASSPORT = 'Passport'
        INT_PASSPORT = 'International Passport'
        RESIDENT_ID = 'Resident_ID'

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        max_length=100,
        help_text="Email",
    )
    is_active = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Телефон')
    firstname = models.CharField(max_length=30, verbose_name='Имя')
    lastname = models.CharField(max_length=30, verbose_name='Фамилия')
    photo = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name='Аватарка')
    region = models.CharField(max_length=100, default=None, null=True, blank=True, verbose_name='Регион')
    sex = models.BooleanField(null=True, blank=True, verbose_name='Пол')
    doc_type = models.CharField(choices=Docs.choices, max_length=30, null=True, blank=True,
                                verbose_name='Тип документа')
    doc_info = models.CharField(max_length=200, null=True, blank=True, verbose_name='Данные о документе')
    is_entity = models.BooleanField(default=False, verbose_name='Юридическое лицо')
    activity = models.CharField(max_length=250, null=True, blank=True, verbose_name='Описание опыта')
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    CV = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name='Резюме')
    activities = models.ManyToManyField(to='ActivityCategory', related_name='users', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    @property
    def is_authenticated(self):
        return self.is_active

    groups = models.ManyToManyField(
        Group,
        blank=False,
        related_name="user_set",
        related_query_name="user",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname', 'groups']

    def __str__(self):
        return str(self.phone_number)


class UserCreateCode(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True, blank=True)


class ActivityCategory(models.Model):
    description = models.CharField(max_length=100)
