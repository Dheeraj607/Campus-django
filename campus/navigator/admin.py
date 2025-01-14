from django.contrib import admin

from .models import Event,  Notification,Request

# Register your models here.

admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(Request)