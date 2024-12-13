from django.contrib import admin
from .models import MaintenanceProvider

class MaintenanceProviderAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'specialization', 'company_registration_number', 'user')
    search_fields = ('company_name', 'company_registration_number')

admin.site.register(MaintenanceProvider, MaintenanceProviderAdmin)

