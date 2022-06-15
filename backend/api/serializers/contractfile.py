from rest_framework import serializers
from system.models import ContractFile


class ContractFileGetSerializer(serializers.ModelSerializer):

    url = serializers.URLField()

    class Meta:
        model = ContractFile
        fields = ["id", "url", "file_hash", "file_name"]


class ContractFileCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = ContractFile
        fields = ["id"]
