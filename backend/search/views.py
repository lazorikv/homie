from system.documents import UserDocument, LandlordDocument, TenantDocument, ApartmentDocument, AddressDocument
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend
from .serializers import UserDocumentSerializer, TenantDocumentSerializer, LandlordDocumentSerializer, \
    ApartmentDocumentSerializer, AddressDocumentSerializer


class UserDocumentView(DocumentViewSet):
    document = UserDocument
    serializer_class = UserDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'username',
    )
    filter_fields = {'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'username': 'username.raw'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'username': 'username.raw'
    }
    # Specify default ordering
    ordering = ('id',)


class LandlordDocumentView(DocumentViewSet):
    document = LandlordDocument
    serializer_class = LandlordDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'first_name',
        "last_name",
        "middle_name",
    )
    filter_fields = {'id': {
        'field': 'id',
        'lookups': [
            LOOKUP_FILTER_RANGE,
            LOOKUP_QUERY_IN,
            LOOKUP_QUERY_GT,
            LOOKUP_QUERY_GTE,
            LOOKUP_QUERY_LT,
            LOOKUP_QUERY_LTE,
        ],
    },
        'user': "user.username",
        'first_name': 'first_name.raw',
        'last_name': 'last_name.raw',
        'middle_name': 'middle_name.raw',
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }
    # Specify default ordering
    ordering = ('id',)


class TenantDocumentView(DocumentViewSet):
    document = TenantDocument
    serializer_class = TenantDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'first_name',
        "last_name",
        "middle_name",
        'username'
    )
    filter_fields = {'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'user': "user.username",
        'first_name': 'first_name.raw',
        'last_name': 'last_name.raw',
        'middle_name': 'middle_name.raw',
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
    }
    # Specify default ordering
    ordering = ('id', )


class ApartmentDocumentView(DocumentViewSet):
    document = ApartmentDocument
    serializer_class = ApartmentDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'area',
        'cost',
        'floor',
        'room_count',
        'owner',
        'address',
        'tenant',
    )
    filter_fields = {'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'address.id': "address.id",
        "address.city": "address.city.raw",
        "address.district": "address.district.raw",
        "address.street": "address.street.raw",
        'area': 'area',
        'floor': 'floor',
        'cost': 'cost',
        'room_count': 'room_count'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'floor': 'floor',
        'cost': 'cost',
        'area': 'area',
        'room_count': 'room_count'
    }
    # Specify default ordering
    ordering = ('id', 'floor', 'area', 'cost', 'room_count')


class AddressDocumentView(DocumentViewSet):
    document = AddressDocument
    serializer_class = AddressDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'city',
        'district',
        'street'
    )
    filter_fields = {'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'city': 'city.raw',
        'district': 'district.raw',
        'street': 'street.raw'
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'city': 'city',
        'district': 'district',
        'street': 'street',
        'house_number': 'house_number',
        'apartment_number': 'apartment_number'
    }
    # Specify default ordering
    ordering = ('id',)
