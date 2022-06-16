from rest_framework import viewsets
from system.models import Tenant
from ..serializers.tenant import TenantWriteSerializer, TenantGetSerializer, TenantPatchSerializer


class TenantViewSet(viewsets.ModelViewSet):

    queryset = Tenant.objects.all()
    serializer_class = TenantGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return TenantWriteSerializer
        elif self.request.method in ("PATCH",):
            return TenantPatchSerializer
        return self.serializer_class

