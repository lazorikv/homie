from rest_framework import viewsets
from system.models import Address
from ..serializers.address import AddressWriteSerializer, AddressGetSerializer, AddressPatchSerializer


class AddressViewSet(viewsets.ModelViewSet):

    queryset = Address.objects.all()
    serializer_class = AddressGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return AddressWriteSerializer
        elif self.request.method in ("PATCH",):
            return AddressPatchSerializer
        return AddressGetSerializer

