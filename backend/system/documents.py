from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from backend.user.models import User
from .models import Address, Tenant, Landlord, Apartment, ApartmentPhoto, ApartmentHiddenPhoto, UtilityBills, Contract, \
    ContractFile


@registry.register_document
class UserDocument(Document):
    id = fields.IntegerField(attr='id')
    username = fields.TextField(
        attr='username',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = User


@registry.register_document
class LandlordDocument(Document):
    id = fields.IntegerField()
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(attr='username',
                                     fields={
                                         'raw': fields.KeywordField(),
                                     }),
        'email': fields.TextField(attr='email',
                                  fields={
                                      'raw': fields.KeywordField(),
                                  }),
        'is_staff': fields.BooleanField(),
        'is_superuser': fields.BooleanField(),
        'is_active': fields.BooleanField()
    })
    first_name = fields.TextField(
        attr='first_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    last_name = fields.TextField(
        attr='last_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    middle_name = fields.TextField(
        attr='middle_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    gender = fields.TextField(attr='gender_to_string')

    class Index:
        name = 'landlords'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Landlord

    related_models = [User]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(LandlordDocument, self).get_queryset().select_related(
            'user'
        )


@registry.register_document
class TenantDocument(Document):
    id = fields.IntegerField()
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(attr='username',
                                     fields={
                                         'raw': fields.KeywordField(),
                                     }),
        'email': fields.TextField(attr='email',
                                  fields={
                                      'raw': fields.KeywordField(),
                                  }),
        'is_staff': fields.BooleanField(),
        'is_superuser': fields.BooleanField(),
        'is_active': fields.BooleanField()
    })
    first_name = fields.TextField(
        attr='first_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    last_name = fields.TextField(
        attr='last_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    middle_name = fields.TextField(
        attr='middle_name',
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    gender = fields.TextField(attr='gender_to_string')

    class Index:
        name = 'tenants'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Tenant

    related_models = [User]


@registry.register_document
class ApartmentDocument(Document):
    id = fields.IntegerField(attr='id')
    tenant = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(attr='first_name',
                                       fields={
                                           'raw': fields.KeywordField(),
                                       }),
        'last_name': fields.TextField(attr='last_name',
                                      fields={
                                          'raw': fields.KeywordField(),
                                      }),
        'middle_name': fields.TextField(attr='middle_name',
                                        fields={
                                            'raw': fields.KeywordField(),
                                        })
    })
    owner = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(attr='first_name',
                                       fields={
                                           'raw': fields.KeywordField(),
                                       }),
        'last_name': fields.TextField(attr='last_name',
                                      fields={
                                          'raw': fields.KeywordField(),
                                      }),
        'middle_name': fields.TextField(attr='middle_name',
                                        fields={
                                            'raw': fields.KeywordField(),
                                        })
    })

    address = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'city': fields.TextField(attr='city',
                                 fields={
                                     'raw': fields.KeywordField(),
                                 }),
        'district': fields.TextField(attr='district',
                                     fields={
                                         'raw': fields.KeywordField(),
                                     }),
        'street': fields.TextField(attr='street',
                                   fields={
                                       'raw': fields.KeywordField(),
                                   }),

    })
    cost = fields.DoubleField(
        attr='cost'
    )
    area = fields.FloatField(
        attr='area'
    )
    floor = fields.IntegerField(
        attr='floor'
    )
    room_count = fields.IntegerField(
        attr='room_count'
    )

    class Index:
        name = 'apartments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Apartment


@registry.register_document
class AddressDocument(Document):
    id = fields.IntegerField(attr='id')

    city = fields.TextField(attr='city',
                            fields={
                                'raw': fields.TextField(analyzer='keyword'),
                            }
                            )
    district = fields.TextField(attr='district',
                                fields={
                                    'raw': fields.TextField(analyzer='keyword'),
                                }
                                )
    street = fields.TextField(attr='street',
                              fields={
                                  'raw': fields.TextField(analyzer='keyword'),
                              }
                              )
    house_number = fields.TextField(attr='house_number',
                                    fields={
                                        'raw': fields.TextField(analyzer='keyword'),
                                    }
                                    )
    apartment_number = fields.TextField(attr='apartment_number',
                                        fields={
                                            'raw': fields.TextField(analyzer='keyword'),
                                        }
                                        )

    class Index:
        name = 'addresses'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Address
