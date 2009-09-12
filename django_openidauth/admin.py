from django.contrib import admin
from django_openidauth.models import UserOpenID


class UserOpenIDAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UserOpenID, UserOpenIDAdmin)
