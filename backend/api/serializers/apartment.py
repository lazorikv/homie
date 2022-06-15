import datetime
import io

import boto3
from PIL import Image
from rest_framework import serializers
from system.models import Address, Apartment, Tenant, Landlord, ApartmentPhoto
from ..serializers.tenant import TenantCutSerializer, TenantGetSerializer
from ..serializers.address import AddressGetSerializer, AddressCutSerializer
from ..serializers.landlord import LandlordCutSerializer, LandlordGetSerializer
from ..serializers.apartmentimages import ApartmentPhotoGetSerializer
from backend import settings
from api.utils import upload_file


class ApartmentWriteSerializer(serializers.ModelSerializer):

    apartment_images = serializers.ListField(write_only=True)
    tenant = TenantCutSerializer()
    owner = LandlordCutSerializer()
    address = AddressCutSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "apartment_images", "tenant", "owner", "address"]

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
        images_data = validated_data.pop("apartment_images", None)
        if not images_data:
            raise TypeError('Apartment must have images.')
        apartment = Apartment.objects.create(**validated_data)
        bucket_name = settings.BUCKET_NAME
        apartment.tenant = tenant
        apartment.owner = landlord
        apartment.address = address
        for image in images_data:
            object_name = str(image.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
            upload_data = upload_file(path=str(image.file.name), bucket=bucket_name,
                                      object_name="apartment_images/" + object_name)
            if not upload_data:
                raise ValueError("Error with upload file to s3")
            url = "https://homieproject.s3.amazonaws.com/apartment_images/" + object_name
            image = ApartmentPhoto.objects.create(url=url, apartment=apartment, image_name=object_name)
            image.save()

        apartment.save()
        return apartment


class ApartmentGetSerializer(serializers.ModelSerializer):

    apartment_images = ApartmentPhotoGetSerializer(many=True)
    tenant = TenantGetSerializer()
    owner = LandlordGetSerializer()
    address = AddressGetSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "apartment_images", "tenant", "owner", "address"]


class ApartmentCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost"]


class ApartmentPatchSerializer(serializers.ModelSerializer):

    apartment_images = serializers.ListField(write_only=True)
    tenant = TenantCutSerializer()
    owner = LandlordCutSerializer()
    address = AddressCutSerializer()

    class Meta:
        model = Apartment
        fields = ["id", "floor", "room_count", "area", "cost", "apartment_images", "tenant", "owner", "address"]

    def update(self, instance, validated_data):
        # S3 bucket connection
        s3_client = boto3.client("s3",
                                 aws_access_key_id=settings.USER_ACCESS_ID,
                                 aws_secret_access_key=settings.USER_ACCESS_KEY)

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
        images_data = validated_data.pop("apartment_images", None)
        if not address_data:
            raise TypeError('Apartment must have images.')

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        bucket_name = settings.BUCKET_NAME
        if images_data:
            old_images = ApartmentPhoto.objects.filter(apartment_id=instance.id)
            for image in old_images:
                s3_client.delete_object(Bucket=bucket_name, Key='apartment_images/' + image.image_name)
            old_images.delete()
            for image in images_data:
                object_name = str(image.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
                upload_data = upload_file(path=str(image.file.name), bucket=bucket_name,
                                          object_name="apartment_images/" + object_name)
                if not upload_data:
                    raise ValueError("Error with upload file to s3")
                url = "https://homieproject.s3.amazonaws.com/apartment_images/" + object_name
                image = ApartmentPhoto.objects.create(url=url, apartment=instance, image_name=object_name)
                image.save()
                instance.apartment_images.add(image)
        instance.tenant = tenant
        instance.address = address
        instance.owner = landlord

        instance.save()
        return instance


class ApartmentForOtherSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = Apartment
        fields = ["id"]
