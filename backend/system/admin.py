from django.contrib import admin
from .models import Tenant, Address, Landlord, Apartment, UtilityBills, Contract

admin.site.register(Address)
admin.site.register(Tenant)
admin.site.register(Landlord)
admin.site.register(Apartment)
admin.site.register(UtilityBills)
admin.site.register(Contract)
