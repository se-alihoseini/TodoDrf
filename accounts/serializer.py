from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['password'] != data['password2']:
            return serializers.ValidationError('password doesnt match')
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=200)
    password = serializers.CharField(required=True, max_length=200)
