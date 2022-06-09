from rest_framework import serializers
from system.models import Landlord, Tenant, Apartment, Contract
from ..serializers import tenant, apartment, landlord


class ContractWriteSerializer(serializers.ModelSerializer):

    contract_file = serializers.URLField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentCutSerializer()

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment"]

    def create(self, validated_data):
        tenant_data = validated_data.pop("tenant", None)
        tenant = Tenant.objects.get(id=tenant_data["id"])
        landlord_data = validated_data.pop("owner", None)
        landlord = Landlord.objects.get(id=landlord_data["id"])
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])
        contract = Contract.objects.create(tenant=tenant, owner=landlord, apartment=apartment, **validated_data)
        contract.save()

        return contract


class ContractGetSerializer(serializers.ModelSerializer):

    contract_file = serializers.URLField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentCutSerializer()

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment"]


class ContractPatchSerializer(serializers.ModelSerializer):

    contract_file = serializers.URLField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentCutSerializer()

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment"]

    def update(self, instance, validated_data):
        tenant_data = validated_data.pop("tenant", None)
        tenant = Tenant.objects.get(id=tenant_data["id"])
        landlord_data = validated_data.pop("owner", None)
        landlord = Landlord.objects.get(id=landlord_data["id"])
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.tenant = tenant
        instance.owner = landlord
        instance.apartment = apartment
        instance.save()
        return instance
