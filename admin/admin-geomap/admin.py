from django.contrib import admin
from django_admin_geomap import ModelAdmin

from models import *


@admin.register(Target)
class TargetAdmin(ModelAdmin):
    actions = None
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    geomap_autozoom = "10"
    list_display = ('id', 'name', 'photo', 'time', 'radius', 'lat', 'lon', 'if_season')


@admin.register(SolutionTarget)
class CompleteAdmin(admin.ModelAdmin):
    list_display = ('relation', 'target', 'photo', 'verdict', 'desc')
