from rest_framework import viewsets
from system.models import Landlord
from ..serializers.landlord import LandlordWriteSerializer, LandlordGetSerializer, LandlordPatchSerializer


class LandlordViewSet(viewsets.ModelViewSet):

    queryset = Landlord.objects.all()
    serializer_class = LandlordGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return LandlordWriteSerializer
        elif self.request.method in ("PATCH",):
            return LandlordPatchSerializer
        return self.serializer_class
