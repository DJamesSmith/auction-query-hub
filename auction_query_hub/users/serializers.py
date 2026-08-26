from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    username: serializers.CharField = serializers.CharField(min_length=3, max_length=150)
    email: serializers.EmailField = serializers.EmailField()
    password: serializers.CharField = serializers.CharField(min_length=6, write_only=True)
    role: serializers.ChoiceField = serializers.ChoiceField(choices=User.Role.choices)

    class Meta:
        model: User = User
        fields: tuple[str, ...] = ("id", "username", "email", "password", "role",)

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError( {"username": "A user with this username already exists." })
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError( {"email": "A user with this email address already exists." })
        return attrs


    def validate_username(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Username is required.")
        if len(value) < 3:
            raise serializers.ValidationError("Username must contain at least 3 characters.")
        return value


    def validate_email(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Email address is required.")
        return value


    def validate_password(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 6:
            raise serializers.ValidationError("Password must contain at least 6 characters.")
        return value


    def validate_role(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Please select a role.")
        if value not in User.Role.values:
            raise serializers.ValidationError("Invalid user role.")
        return value


# NOTE:
# password: serializers.CharField = serializers.CharField(min_length=6, write_only=True)
# means:
# The client can send password in a POST.
# DRF will use it during validation/deserialization.
# DRF will never include it in serialized response data.