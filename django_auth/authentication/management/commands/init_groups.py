import logging

from django.core.management import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model

from django_base.settings import GROUPS

User = get_user_model()


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)
            for app_model in GROUPS[group_name]:
                for permission_name in GROUPS[group_name][app_model]:
                    name = f"Can {permission_name} {app_model}"
                    logging.info(f"Creating {name}")
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue
                    new_group.permissions.add(model_add_perm)