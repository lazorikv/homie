from rest_framework import serializers
from system.models import ApartmentPhoto, ApartmentHiddenPhoto


class ApartmentPhotoGetSerializer(serializers.ModelSerializer):

    url = serializers.URLField()

    class Meta:
        model = ApartmentPhoto
        fields = ["id", "url", "image_name"]


class ApartmentPhotoCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = ApartmentPhoto
        fields = ["id"]


class ApartmentHiddenPhotoGetSerializer(serializers.ModelSerializer):

    url = serializers.URLField()

    class Meta:
        model = ApartmentPhoto
        fields = ["id", "url", "image_name"]


class ApartmentHiddenPhotoCutSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = ApartmentPhoto
        fields = ["id"]

