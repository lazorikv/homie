from rest_framework import serializers
from system.models import Address


class AddressWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["id", "city", "district", "street", "house_number", "apartment_number"]

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)
        address.save()
        return address


class AddressPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["id", "city", "district", "street", "house_number", "apartment_number"]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AddressGetSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Address
        fields = ["id", "city", "district", "street", "house_number", "apartment_number"]


class AddressCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Address
        fields = ["id"]
