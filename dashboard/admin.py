from django.contrib import admin
from .models import Autor
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(Autor)
except AlreadyRegistered:
    pass
