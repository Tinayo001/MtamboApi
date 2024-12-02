from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from .models import User

from .serializers import (
    UserSerializer,
    UserSignupSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Token generation function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


# Custom JWT Token View
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# User Signup View
class SignupView(APIView):
    @extend_schema(
        request=UserSignupSerializer,
        responses={201: UserSerializer},
        description="Create a new user account"
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({"message": "User created successfully", "tokens": tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View
class LoginView(APIView):
    """
    Authenticate a user with their email and password, and return JWT tokens.
    """
    @extend_schema(
        request=UserSignupSerializer,
        responses={200: "Access and Refresh Tokens"},
        description="Authenticate a user and provide JWT tokens"
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to retrieve the user from the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is active
        if not user.is_active:
            return Response({"error": "Account is not active"}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate the password
        if user.check_password(password):
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
# Update User View
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: UserSerializer},
        description="Update user account details"
    )
    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User details updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Change Password View
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: "Password changed successfully"},
        description="Change the password for the authenticated user"
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete User View
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Delete the authenticated user's account",
        responses={204: "No content"}
    )
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Admin-Only User List View
class ListUsersView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: UserSerializer(many=True)},
        description="List all users (Admin only)"
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Password Reset Request View
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: "Password reset email sent successfully."},
        description="Request a password reset by providing a valid email."
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                reset_token = RefreshToken.for_user(user).access_token
                reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link below to reset your password:\n{reset_url}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Password Reset View
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetSerializer,
        responses={200: "Password has been reset successfully."},
        description="Reset the password using a valid token and a new password."
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

