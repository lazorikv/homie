from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from system.documents import UserDocument, LandlordDocument, TenantDocument, ApartmentDocument, AddressDocument


class UserDocumentSerializer(DocumentSerializer):
    class Meta:
        document = UserDocument

        fields = (
            'id',
            'username',
            'email',
            'is_staff',
            'is_superuser',
            'is_active'
        )


class LandlordDocumentSerializer(DocumentSerializer):
    class Meta:
        document = LandlordDocument

        fields = (
            "id",
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'user'
        )


class TenantDocumentSerializer(DocumentSerializer):
    class Meta:
        document = TenantDocument

        fields = (
            "id",
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'gender',
            'user'
        )


class ApartmentDocumentSerializer(DocumentSerializer):

    class Meta:
        document = ApartmentDocument

        fields = (
            "id",
            "cost",
            "floor",
            "area",
            "room_count",
            "owner",
            "tenant",
            "address",
        )


class AddressDocumentSerializer(DocumentSerializer):

    class Meta:
        document = AddressDocument

        fields = (
            "id",
            "city",
            "district",
            "street",
            "house_number",
            "apartment_number"
        )
