from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import AccountType, User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.password_validation import validate_password
from Maintenance_Company.models import MaintenanceProvider
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'account_type', 'created_at']


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'account_type')

    def validate_account_type(self, value):
        """
        Ensure the account type is valid at the time of creation.
        """
        if value not in [choice[0] for choice in User.AccountType.choices]:
            raise serializers.ValidationError("Invalid account type selected.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.is_active = True  # Ensure the user is active
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details.
    Supports partial updates.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'account_type']

    def validate_account_type(self, value):
        """
        Validate that the account type is valid.
        """
        valid_choices = [choice[0] for choice in User._meta.get_field('account_type').choices]
        if value not in valid_choices:
            raise serializers.ValidationError("Invalid account type")
        return value



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context.get("user")
        # Check if the old password is correct
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password")
        return value

    def validate_new_password(self, value):
        # Ensure the new password is not the same as the old one (optional)
        user = self.context.get("user")
        if user.check_password(value):
            raise serializers.ValidationError("New password cannot be the same as the old password")
        
        # Add any other password validation here (e.g., length, complexity)

        return value

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the database.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        """
        Validate the reset token and ensure the user exists.
        """
        token = data['token']
        try:
            user = RefreshToken(token).payload.get('user_id')
            data['user'] = User.objects.get(id=user)
        except Exception:
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        return data
