from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from .models import Event, Notification,Request


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)# Add full_name field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name','last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before creating user

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        return user


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'date_created', 'message','type']
        read_only_fields = ['date_created']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



class RequestSerializer(serializers.ModelSerializer):
    # import pdb; pdb.set_trace()
    req_from = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.IntegerField(default=0)
    username = serializers.CharField(source='req_from.username', read_only=True)

    class Meta:
        model = Request
        fields = [
            'id', 'req_from', 'message', 'date',
            'from_time', 'to_time', 'date_created',
            'status', 'replay','username'
        ]
        read_only_fields = ['id', 'date_created', 'status', 'replay']

    def create(self, validated_data):
        # Ensure the status is set to 0 ("Pending") regardless of input
        validated_data['status'] = 0
        return super().create(validated_data)