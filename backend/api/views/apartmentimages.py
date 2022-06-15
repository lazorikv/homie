from rest_framework import viewsets
from system.models import ApartmentPhoto, ApartmentHiddenPhoto

from ..serializers.apartmentimages import ApartmentPhotoGetSerializer, ApartmentHiddenPhotoGetSerializer


class ApartmentPhotoViewSet(viewsets.ModelViewSet):

    queryset = ApartmentPhoto.objects.all()
    serializer_class = ApartmentPhotoGetSerializer


class ApartmentHiddenPhotoViewSet(viewsets.ModelViewSet):

    queryset = ApartmentHiddenPhoto.objects.all()
    serializer_class = ApartmentHiddenPhotoGetSerializer
