from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from account.models import User

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    token = serializers.JSONField(read_only=True)

    def get_token(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        username = validated_data['username']

        if User.objects.filter(email=email).exists():
            user = authenticate(username=email, password=password)
            if user:
                return {'token':self.get_token(validated_data)}
            else:
                raise serializers.ValidationError('Invalid password')
        else:
            user = User.objects.create_user(email=email, password=password, username=username)
            return {'token':self.get_token(validated_data)}


