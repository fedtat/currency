from currency.models import ContactUs, Source

from django.contrib import admin

from rangefilter.filters import DateRangeFilter


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'code_name',
        'icon',
    )
    readonly_fields = (
        'id',
        'code_name',
    )
    search_fields = ['name']


admin.site.register(Source, SourceAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'name',
        'email_from',
    )
    list_filter = (
        'email_from',
        ('created', DateRangeFilter),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ContactUs, ContactUsAdmin)
