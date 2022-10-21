from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Business)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Cart)

