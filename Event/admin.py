from atexit import register
from django.contrib import admin

from Event.models import Camp, Event

# Register your models here.
admin.site.register(Event)