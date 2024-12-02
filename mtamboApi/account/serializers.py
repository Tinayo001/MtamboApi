from rest_framework import serializers
from .models import AccountType, User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


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

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.is_active = True  # Ensure the user is active
        user.save()
        return user


def create(self, validated_data):
    """
    Create a user with the provided validated data.
    """
    # Generate username if not provided
    username = validated_data.get('username', None)
    if not username:
        # Generate the username based on first_name and last_name (or any other logic you want)
        user_instance = User(**validated_data)
        username = user_instance.generate_username()

    # Create the user
    user = User.objects.create_user(
        username=username,  # Use the generated or provided username
        email=validated_data['email'],
        password=validated_data['password'],  # Automatically hashes the password
        first_name=validated_data.get('first_name', ''),
        last_name=validated_data.get('last_name', ''),
        phone_number=validated_data.get('phone_number', ''),
        account_type=validated_data.get('account_type', ''),

    )
    user.set_password(validated_data['password'])  # Ensure password is hashed
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
        if value not in [choice[0] for choice in User.AccountType.choices]:
            raise serializers.ValidationError("Invalid account type")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(write_only=True, min_length=8)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        """
        Validate that the old password is correct.
        """
        user = self.context['user']
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect password"})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password"})
        return data

    def save(self):
        """
        Save the new password for the user.
        """
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
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

