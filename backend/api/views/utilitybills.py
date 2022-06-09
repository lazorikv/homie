from rest_framework import viewsets
from system.models import UtilityBills
from ..serializers.utilitybills import UtilityBillsWriteSerializer, \
    UtilityBillsGetSerializer, UtilityBillsPatchSerializer


class UtilityBillsViewSet(viewsets.ModelViewSet):

    queryset = UtilityBills.objects.all()
    serializer_class = UtilityBillsGetSerializer

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return UtilityBillsWriteSerializer
        elif self.request.method in ("PATCH",):
            return UtilityBillsPatchSerializer
        return self.serializer_class
