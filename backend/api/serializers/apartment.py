from rest_framework import serializers
from system.models import Address, Apartment, Tenant, Landlord
from ..serializers.tenant import TenantCutSerializer
from ..serializers.address import AddressGetSerializer, AddressCutSerializer
from ..serializers.landlord import LandlordCutSerializer


class ApartmentWriteSerializer(serializers.ModelSerializer):

    photo = serializers.URLField()
    hidden_photo = serializers.URLField()
    tenant = TenantCutSerializer()
    owner = LandlordCutSerializer()
    address = AddressGetSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "photo", "hidden_photo", "tenant", "owner", "address"]

    def create(self, validated_data):

        tenant_data = validated_data.pop("tenant", None)
        if not tenant_data:
            raise TypeError('Apartment must have relation to tenant.')
        tenant = Tenant.objects.get(id=tenant_data["id"])

        landlord_data = validated_data.pop("owner", None)
        if not landlord_data:
            raise TypeError('Apartment must have relation to landlord.')
        landlord = Landlord.objects.get(id=landlord_data["id"])

        address_data = validated_data.pop("address", None)
        if not address_data:
            raise TypeError('Apartment must have relation to address.')
        address = Address.objects.get(id=address_data["id"])

        apartment = Apartment.objects.create(**validated_data)
        apartment.tenant = tenant
        apartment.owner = landlord
        apartment.address = address
        apartment.save()
        return apartment


class ApartmentGetSerializer(serializers.ModelSerializer):

    photo = serializers.URLField()
    hidden_photo = serializers.URLField()
    tenant = TenantCutSerializer()
    owner = LandlordCutSerializer()
    address = AddressGetSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "photo", "hidden_photo", "tenant", "owner", "address"]


class ApartmentCutSerializer(serializers.ModelSerializer):

    photo = serializers.URLField()
    hidden_photo = serializers.URLField()
    id = serializers.IntegerField()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "photo", "hidden_photo"]


class ApartmentPatchSerializer(serializers.ModelSerializer):

    photo = serializers.URLField()
    hidden_photo = serializers.URLField()
    tenant = TenantCutSerializer()
    owner = LandlordCutSerializer()
    address = AddressCutSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "photo", "hidden_photo", "tenant", "owner", "address"]

    def update(self, instance, validated_data):
        tenant_data = validated_data.pop("tenant", None)
        if not tenant_data:
            raise TypeError('Apartment must have relation to tenant.')
        tenant = Tenant.objects.get(id=tenant_data["id"])

        landlord_data = validated_data.pop("owner", None)
        if not landlord_data:
            raise TypeError('Apartment must have relation to landlord.')
        landlord = Landlord.objects.get(id=landlord_data["id"])

        address_data = validated_data.pop("address", None)
        if not address_data:
            raise TypeError('Apartment must have relation to address.')
        address = Address.objects.get(id=address_data["id"])

        instance.tenant = tenant
        instance.address = address
        instance.owner = landlord

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
