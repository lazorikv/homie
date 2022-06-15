from rest_framework import serializers
from system.models import Landlord
from backend.user.serializers import UserSerializer, UserGetSerializer, UserCutSerializer
from backend.user.models import User


class LandlordWriteSerializer(serializers.ModelSerializer):

    user = UserCutSerializer()

    class Meta:
        model = Landlord
        fields = ["first_name", "last_name", "middle_name", "gender", "phone_number", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user", None)
        user = User.objects.get(id=user_data["id"])
        landlord = Landlord.objects.create(user=user, **validated_data)
        landlord.save()
        return landlord


class LandlordGetSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Landlord
        fields = ["id", "first_name", "last_name", "middle_name", "gender", "phone_number", "user"]


class LandlordPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Landlord
        fields = ["first_name", "last_name", "middle_name", "gender", "phone_number"]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LandlordCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Landlord
        fields = ["id"]
