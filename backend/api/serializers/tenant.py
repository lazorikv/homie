from rest_framework import serializers
from system.models import Tenant
from backend.user.serializers import UserSerializer
from backend.user.models import User


class TenantWriteSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Tenant
        fields = ["id", "first_name", "last_name", "middle_name", "gender", "phone_number", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user", None)
        user = User.objects.get(id=user_data["id"])
        tenant = Tenant.objects.create(user=user, **validated_data)
        tenant.save()
        return tenant


class TenantGetSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Tenant
        fields = ["id", "first_name", "last_name", "middle_name", "gender", "phone_number", "user"]


class TenantPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = ["first_name", "last_name", "middle_name", "gender", "phone_number"]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class TenantCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Tenant
        fields = ["id"]
