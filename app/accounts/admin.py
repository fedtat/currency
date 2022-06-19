from accounts.models import User

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
