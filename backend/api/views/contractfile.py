from rest_framework import viewsets
from system.models import ContractFile
from ..serializers.contractfile import ContractFileGetSerializer


class ContractFileViewSet(viewsets.ModelViewSet):

    queryset = ContractFile.objects.all()
    serializer_class = ContractFileGetSerializer

