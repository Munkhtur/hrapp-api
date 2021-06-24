from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=20, min_length=4)
    full_name = serializers.CharField(max_length=30, min_length=2)
    password = serializers.CharField(
        max_length=20, min_length=4, write_only=True)
    department = serializers.CharField(max_length=30, min_length=2)
    total_hours = serializers.FloatField(default=0)
    is_active = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')
        full_name = attrs.get('full_name', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use'})

        if User.objects.filter(full_name=full_name).exists():
            raise serializers.ValidationError(
                {'fullname': 'Name already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.total_hours = validated_data.get(
    #         'total_hours', instance.total_hours)
    #     instance.save()
    #     return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=20, min_length=4, write_only=True)
    email = serializers.EmailField(max_length=20, min_length=4)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'total_hours']

    def update(self, instance, validated_data):
        instance.total_hours = validated_data.get(
            'total_hours', instance.total_hours)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['old_password', 'new_password']
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
