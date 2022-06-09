from rest_framework import viewsets
from system.models import Contract
from ..serializers.contract import ContractWriteSerializer, ContractGetSerializer, ContractPatchSerializer


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return ContractWriteSerializer
        elif self.request.method in ("PATCH",):
            return ContractPatchSerializer
        return self.serializer_class
