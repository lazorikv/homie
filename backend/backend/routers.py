from rest_framework.routers import SimpleRouter
from django.urls import path, include
from backend.user.views import UserViewSet
from backend.auth.views import LoginViewSet, RegistrationViewSet, RefreshViewSet, ChangePasswordView
from api.views import address, tenant, landlord, apartment, contract, utilitybills, contractfile, apartmentimages
from search.views import UserDocumentView, LandlordDocumentView, TenantDocumentView, ApartmentDocumentView, AddressDocumentView

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register(r'auth/change_password', ChangePasswordView, basename='auth_change_password'),


# USER
routes.register(r'user', UserViewSet, basename='user')

# ADDRESS
routes.register(r"address", address.AddressViewSet, basename='address')

# TENANT
routes.register(r"tenant", tenant.TenantViewSet, basename='tenant')

# LANDLORD
routes.register(r"landlord", landlord.LandlordViewSet, basename='landlord')

# APARTMENT
routes.register(r"apartment", apartment.ApartmentViewSet, basename='apartment')

# CONTRACT
routes.register(r"contract", contract.ContractViewSet, basename='contract')

# CONTRACT
routes.register(r"utilitybills", utilitybills.UtilityBillsViewSet, basename='utilitybills')

# CONTRACT FILE
routes.register(r"contractfile", contractfile.ContractFileViewSet, basename='contractfile')

# APARTMENT IMAGES
routes.register(r"apartmentimage", apartmentimages.ApartmentPhotoViewSet, basename='apartmentimage')

# APARTMENT HIDDEN IMAGES
routes.register(r"apartmenthiddenimage", apartmentimages.ApartmentHiddenPhotoViewSet, basename='apartmenthiddenimage')

# ELASTICSEARCH
routes.register(r"search-user", UserDocumentView, basename='search-user')
routes.register(r"search-landlord", LandlordDocumentView, basename='search-landlord')
routes.register(r"search-tenant", TenantDocumentView, basename='search-tenant')
routes.register(r"search-apartment", ApartmentDocumentView, basename='search-apartment')
routes.register(r"search-address", AddressDocumentView, basename='search-address')

urlpatterns = [
    *routes.urls,
]
