from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'note',
            'twitter',
        ]


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'profile'
        ]

    def update(self, instance, validate_data):
        profile = validate_data.pop('profile')
        profile_serializer = ProfileSerializer(instance.profile, data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile.save()
        return super(UserSerializer, self).update(instance, validate_data)


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password'
        ]

    def validate(self, attr):
        validate_password(attr['password'])
        return attr

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
