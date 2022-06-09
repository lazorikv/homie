from backend.user.serializers import UserSerializer, UserPatchSerializer
from backend.user.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete', 'patch']
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PATCH',):
            return UserPatchSerializer
        return self.serializer_class

