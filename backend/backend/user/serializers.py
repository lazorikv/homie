from rest_framework import serializers
from backend.user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser', "is_active"]


class UserPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser', "is_active"]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserGetSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser', "is_active"]


class UserCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id"]
