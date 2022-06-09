from rest_framework import serializers
from system.models import UtilityBills, Apartment
from ..serializers.apartment import ApartmentCutSerializer, ApartmentGetSerializer


class UtilityBillsWriteSerializer(serializers.ModelSerializer):

    apartment = ApartmentCutSerializer()

    class Meta:
        model = UtilityBills
        fields = ["id", "gas_supply", "water_supply", "electricity", "apartment"]

    def create(self, validated_data):
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])
        utility_bills = UtilityBills.objects.create(apartment=apartment, **validated_data)
        utility_bills.save()
        return utility_bills


class UtilityBillsGetSerializer(serializers.ModelSerializer):

    apartment = ApartmentGetSerializer()

    class Meta:
        model = UtilityBills
        fields = ["id", "gas_supply", "water_supply", "electricity", "apartment"]


class UtilityBillsPatchSerializer(serializers.ModelSerializer):

    apartment = ApartmentCutSerializer()

    class Meta:
        model = UtilityBills
        fields = ["id", "gas_supply", "water_supply", "electricity", "apartment"]

    def update(self, instance, validated_data):
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.apartment = apartment
        instance.save()
        return instance

