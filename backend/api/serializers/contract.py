import datetime
import boto3
from rest_framework import serializers
from system.models import Landlord, Tenant, Apartment, Contract, ContractFile
from backend import settings
from ..serializers.contractfile import ContractFileGetSerializer, ContractFileCutSerializer
from ..serializers import tenant, apartment, landlord
from api.utils import upload_file


class ContractWriteSerializer(serializers.ModelSerializer):
    contract_file = serializers.FileField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentForOtherSerializer()

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
        file_data = validated_data.pop("contract_file", None)
        contract = Contract.objects.create(tenant=tenant, owner=landlord, apartment=apartment, **validated_data)
        if not file_data:
            raise ValueError("File is not attached")
        file_hash = hash(file_data)
        bucket_name = settings.BUCKET_NAME
        object_name = str(file_data.name).replace(" ", "") + str(datetime.datetime.now().strftime('%H_%M_%S'))
        upload_data = upload_file(path=str(file_data.file.name), bucket=bucket_name, object_name=object_name)
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

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment"]


class ContractPatchSerializer(serializers.ModelSerializer):
    contract_file = serializers.FileField()
    tenant = tenant.TenantCutSerializer()
    owner = landlord.LandlordCutSerializer()
    apartment = apartment.ApartmentForOtherSerializer()

    class Meta:
        model = Contract
        fields = ["id", "contract_file", "is_active", "owner", "tenant", "apartment"]

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
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        bucket_name = settings.BUCKET_NAME

        old_file = ContractFile.objects.get(contract_id=instance.id)
        s3_client.delete_object(Bucket=bucket_name, Key='contracts/' + old_file.file_name)
        old_file.delete()
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
