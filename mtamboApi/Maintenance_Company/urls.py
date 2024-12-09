from . import views
from django.urls import path
from .views.maintenance_provider_views import MaintenanceCompanyAPIView

urlpatterns = [
        path('maintenance_company/', views.MaintenanceCompanyAPIView.as_view(), name='Maintenance_Company'),  # GET, POST, PUT)
        ]
