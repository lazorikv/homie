from rest_framework import viewsets
from system.models import Apartment
from ..serializers.apartment import ApartmentWriteSerializer, ApartmentGetSerializer, ApartmentPatchSerializer


class ApartmentViewSet(viewsets.ModelViewSet):

    queryset = Apartment.objects.all()
    serializer_class = ApartmentGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return ApartmentWriteSerializer
        elif self.request.method in ("PATCH",):
            return ApartmentPatchSerializer
        return self.serializer_class
