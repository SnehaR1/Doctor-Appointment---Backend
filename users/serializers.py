from rest_framework import serializers
from .models import UserData


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserData
        fields = ["username", "phone", "email", "password", "confirm_password"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        phone = validated_data["phone"]
        password = validated_data["password"]
        confirm_password = validated_data["confirm_password"]
        if not email:
            raise serializers.ValidationError(
                {"email": "Email Field should not be null"}
            )
        if not password:
            raise serializers.ValidationError(
                {"password": "Password Field should be null"}
            )
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({"passwords": "Passwords do no match"})
        user = UserData.objects.create_user(
            email, password, username=username, phone=phone
        )

        return user
