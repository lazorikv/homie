import datetime
import boto3
from rest_framework import serializers
from system.models import Landlord, Tenant, Apartment, Contract, ContractFile, ApartmentHiddenPhoto
from backend import settings
from ..serializers.contractfile import ContractFileGetSerializer
from ..serializers.apartmentimages import ApartmentHiddenPhotoGetSerializer
from ..serializers import tenant, apartment, landlord
from api.utils import upload_file


class ContractWriteSerializer(serializers.ModelSerializer):
    contract_file = serializers.FileField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentForOtherSerializer()
    apartment_hidden_images = serializers.ListField(write_only=True)

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment", "apartment_hidden_images"]

    def create(self, validated_data):
        tenant_data = validated_data.pop("tenant", None)
        tenant = Tenant.objects.get(id=tenant_data["id"])
        landlord_data = validated_data.pop("owner", None)
        landlord = Landlord.objects.get(id=landlord_data["id"])
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])
        file_data = validated_data.pop("contract_file", None)
        images_data = validated_data.pop("apartment_hidden_images", None)
        bucket_name = settings.BUCKET_NAME
        contract = Contract.objects.create(tenant=tenant, owner=landlord, apartment=apartment, **validated_data)
        if images_data:
            for image in images_data:
                object_name = str(image.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
                upload_data = upload_file(path=str(image.file.name), bucket=bucket_name,
                                          object_name="apartment_hidden_images/" + object_name)
                if not upload_data:
                    raise ValueError("Error with upload file to s3")
                url = "https://homieproject.s3.amazonaws.com/apartment_hidden_images/" + object_name
                image = ApartmentHiddenPhoto.objects.create(url=url, contract=contract, image_name=object_name)
                image.save()
        if not file_data:
            raise ValueError("File is not attached")
        file_hash = hash(file_data)

        object_name = str(file_data.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
        upload_data = upload_file(path=str(file_data.file.name),
                                  bucket=bucket_name, object_name="contracts/" + object_name)
        if not upload_data:
            raise ValueError("Error with upload file to s3")
        url = "https://homieproject.s3.amazonaws.com/contracts/" + object_name
        file = ContractFile.objects.create(url=url, file_hash=file_hash, contract=contract, file_name=object_name)
        file.save()
        contract.save()

        return contract


class ContractGetSerializer(serializers.ModelSerializer):
    contract_file = ContractFileGetSerializer(many=True)
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentCutSerializer()
    apartment_hidden_images = ApartmentHiddenPhotoGetSerializer(many=True)

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment", "apartment_hidden_images"]


class ContractPatchSerializer(serializers.ModelSerializer):
    contract_file = serializers.FileField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentForOtherSerializer()
    apartment_hidden_images = serializers.ListField(write_only=True)

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment", "apartment_hidden_images"]

    def update(self, instance, validated_data):
        # S3 bucket connection
        s3_client = boto3.client("s3",
                                 aws_access_key_id=settings.USER_ACCESS_ID,
                                 aws_secret_access_key=settings.USER_ACCESS_KEY)

        tenant_data = validated_data.pop("tenant", None)
        tenant = Tenant.objects.get(id=tenant_data["id"])
        landlord_data = validated_data.pop("owner", None)
        landlord = Landlord.objects.get(id=landlord_data["id"])
        apartment_data = validated_data.pop("apartment", None)
        apartment = Apartment.objects.get(id=apartment_data["id"])
        file_data = validated_data.pop("contract_file", None)
        images_data = validated_data.pop("apartment_hidden_images", None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        bucket_name = settings.BUCKET_NAME
        old_file = ContractFile.objects.get(contract_id=instance.id)
        s3_client.delete_object(Bucket=bucket_name, Key='contracts/' + old_file.file_name)
        old_file.delete()
        if images_data:
            old_images = ApartmentHiddenPhoto.objects.filter(contract_id=instance.id)
            for image in old_images:
                s3_client.delete_object(Bucket=bucket_name, Key='apartment_hidden_image/' + image.image_name)
            old_images.delete()
            for image in images_data:
                object_name = str(image.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
                upload_data = upload_file(path=str(image.file.name), bucket=bucket_name,
                                          object_name="apartment_hidden_images/" + object_name)
                if not upload_data:
                    raise ValueError("Error with upload file to s3")
                url = "https://homieproject.s3.amazonaws.com/apartment_hidden_images/" + object_name
                image = ApartmentHiddenPhoto.objects.create(url=url, contract=instance, image_name=object_name)
                image.save()

        file_hash = hash(file_data)
        object_name = str(file_data.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
        upload_data = upload_file(path=str(file_data.file.name), bucket=bucket_name,
                                  object_name="contracts/" + object_name)

        if not upload_data:
            raise ValueError("Error with upload file to s3")
        url = "https://homieproject.s3.amazonaws.com/contracts/" + object_name
        file = ContractFile.objects.create(url=url, file_hash=file_hash, contract=instance, file_name=object_name)
        file.save()
        instance.tenant = tenant
        instance.owner = landlord
        instance.apartment = apartment
        instance.contract_file.add(file)
        instance.save()
        return instance


class ContractCutSerializer(serializers.ModelSerializer):
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentForOtherSerializer()

    class Meta:
        model = Contract
        fields = ["id", "is_active", "owner", "tenant", "apartment"]
