from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from backend.user.models import User


class Address(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=10)

    class Meta:
        unique_together = ("city", "district", "street", "house_number", "apartment_number")


class Tenant(models.Model):
    Male = "MALE"
    Female = "FEMALE"
    Undefined = "UNDEFINED"
    GENDER_TYPE = ((Male, "Male"), (Female, "Female"), (Undefined, "Undefined"))
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE, default="Undefined")
    phone_number = PhoneNumberField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant')

    REQUIRED_FIELDS = ['first_name', 'last_name', "phone_number", "middle_name"]


class Landlord(models.Model):
    Male = "MALE"
    Female = "FEMALE"
    Undefined = "UNDEFINED"
    GENDER_TYPE = ((Male, "Male"), (Female, "Female"), (Undefined, "Undefined"))
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE, default="Undefined")
    phone_number = PhoneNumberField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord')

    REQUIRED_FIELDS = ['first_name', 'last_name', "phone_number", "middle_name"]

    class Meta:
        verbose_name = 'Landlord'


class Apartment(models.Model):
    floor = models.IntegerField()
    room_count = models.IntegerField()
    area = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.URLField(unique=True)
    hidden_photo = models.URLField(unique=True)
    tenant = models.OneToOneField(Tenant, on_delete=models.SET_NULL, related_name='rent_apartment', null=True)
    owner = models.OneToOneField(Landlord, on_delete=models.SET_NULL, related_name='owned_apartment', null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, related_name='apartment_address', null=True)


class UtilityBills(models.Model):
    gas_supply = models.DecimalField(max_digits=10, decimal_places=4)
    water_supply = models.DecimalField(max_digits=10, decimal_places=4)
    electricity = models.DecimalField(max_digits=10, decimal_places=4)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='utility_bills')


class Contract(models.Model):
    is_active = models.BooleanField(default=False)
    owner = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='landlord_contract')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant_contract')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='contract')


class ContractFile(models.Model):
    url = models.URLField(unique=True)
    file_hash = models.CharField(max_length=100)
    file_name = models.CharField(max_length=200, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="contract_file")
