from adrf.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.renderers import AdminRenderer, JSONRenderer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from client.api.serializers import UserSerializer, PermissionSerializer, GroupSerializer, UserChangePasswordSerializer



class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, DjangoModelPermissions]
    renderer_classes = [JSONRenderer, AdminRenderer]
    
    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'change_password':
            serializer_class = UserChangePasswordSerializer
        return serializer_class
    
    @action(detail=True, methods=['patch'], url_path='change-password', url_name='change-password')
    async def change_password(self, request, pk=None):
        user = await self.aget_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        await serializer.asave()
        data = await serializer.adata
        return Response(data)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser, DjangoModelPermissions]
    renderer_classes = [JSONRenderer, AdminRenderer]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser, DjangoModelPermissions]
    renderer_classes = [JSONRenderer, AdminRenderer]