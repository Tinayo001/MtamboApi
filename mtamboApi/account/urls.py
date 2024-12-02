from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyTokenObtainPairView,
    SignupView,
    LoginView,
    UpdateUserView,
    ChangePasswordView,
    DeleteUserView,
    ListUsersView,
    PasswordResetRequestView,
    PasswordResetView
)

urlpatterns = [
    # JWT Token Endpoints
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Custom JWT token view
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh view
    
    # User Authentication Endpoints
    path('signup/', SignupView.as_view(), name='signup'),  # User signup
    path('login/', LoginView.as_view(), name='login'),  # User login
    
    # User Profile and Account Management Endpoints
    path('user/update/', UpdateUserView.as_view(), name='update_user'),  # Update user profile
    path('user/change-password/', ChangePasswordView.as_view(), name='change_password'),  # Change password
    path('user/delete/', DeleteUserView.as_view(), name='delete_user'),  # Delete user account
    
    # Admin Endpoints
    path('admin/users/', ListUsersView.as_view(), name='list_users'),  # Admin-only user listing
    
    # Password Reset Endpoints
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),  # Request password reset email
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),  # Reset password using token
]

