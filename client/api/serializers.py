from rest_framework import serializers
from adrf import serializers as adrf_serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

        
User = get_user_model()
        
class ContentTypeSerializer(adrf_serializers.ModelSerializer):
    
    class Meta:
        model = ContentType
        fields = "__all__"
        
class PermissionSerializer(adrf_serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="permissions-detail")
    content_type = ContentTypeSerializer()
    class Meta:
        model = Permission
        fields = "__all__"

class GroupSerializer(adrf_serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="groups-detail")
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = "__all__"

class UserSerializer(adrf_serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="users-detail")
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True, "required": False}}
        
class UserChangePasswordSerializer(adrf_serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}

    async def aupdate(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        await instance.asave()
        return instance