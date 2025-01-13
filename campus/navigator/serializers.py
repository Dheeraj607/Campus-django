from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from .models import Event, Notification


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(required=True)  # Add full_name field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        # Add any custom validation for full_name (if needed)
        if not data['full_name'].strip():
            raise serializers.ValidationError({"full_name": "Full name cannot be empty"})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before creating user

        full_name = validated_data.pop('full_name')  # Extract full_name
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Save the full_name to the user instance (assuming you have a full_name field on the User model)
        user.full_name = full_name
        user.save()

        return user


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'date_created', 'message','type']
        read_only_fields = ['date_created']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)