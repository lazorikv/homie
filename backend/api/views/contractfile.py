from rest_framework import viewsets
from system.models import ContractFile
from ..serializers.contractfile import ContractFileGetSerializer, ContractFileCutSerializer


class ContractFileViewSet(viewsets.ModelViewSet):

    queryset = ContractFile.objects.all()
    serializer_class = ContractFileGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return ContractFileGetSerializer
        elif self.request.method in ("PATCH",):
            return ContractFileGetSerializer
        return ContractFileGetSerializer
