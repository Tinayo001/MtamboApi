from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MaintenanceProvider
from Technicians.models import Technician
from Tasks.models import Task
from rest_framework.permissions import IsAuthenticated

class MaintenanceCompanyDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            maintenance_company = MaintenanceProvider.objects.get(user=request.user)
            num_technicians = Technician.objects.filter(maintenance_company=maintenance_company).count()
            num_tasks = Task.objects.filter(maintenance_company=maintenance_company).count()

            dashboard_data = {
                "company_name": maintenance_company.company_name,
                "specialization": maintenance_company.get_specialization_display(),
                "company_address": maintenance_company.company_address,
                "company_registration_number": maintenance_company.company_registration_number,
                "num_technicians": num_technicians,
                "num_tasks": num_tasks,
            }

            return Response(dashboard_data, status=status.HTTP_200_OK)

        except MaintenanceProvider.DoesNotExist:
            return Response(
                {"detail": "Maintenance company not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

