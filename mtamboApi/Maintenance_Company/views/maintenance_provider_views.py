from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ..models import MaintenanceProvider
from ..serializers import MaintenanceProviderSerializer

class MaintenanceCompanyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MaintenanceProviderSerializer},
        description="Retrieve the maintenance company associated with the authenticated user."
    )
    def get(self, request, *args, **kwargs):
        # Fetch the maintenance company for the authenticated user
        maintenance_company = MaintenanceProvider.objects.filter(user=request.user).first()

        if maintenance_company:
            serializer = MaintenanceProviderSerializer(maintenance_company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Maintenance company not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=MaintenanceProviderSerializer,
        responses={201: MaintenanceProviderSerializer},
        description="Create a maintenance company and associate it with the authenticated user."
    )
    def post(self, request, *args, **kwargs):
        # Check if the user already has a maintenance provider
        if MaintenanceProvider.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "Maintenance company already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new maintenance provider for the user
        serializer = MaintenanceProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=MaintenanceProviderSerializer,
        responses={200: MaintenanceProviderSerializer},
        description="Update the maintenance company associated with the authenticated user."
    )
    def put(self, request, *args, **kwargs):
        # Fetch the existing maintenance company for the user
        maintenance_company = MaintenanceProvider.objects.filter(user=request.user).first()

        if not maintenance_company:
            return Response({"detail": "Maintenance company not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the existing maintenance provider
        serializer = MaintenanceProviderSerializer(maintenance_company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

