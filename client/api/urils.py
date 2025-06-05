from rest_framework.routers import DefaultRouter
from client.api.views import UserViewSet, PermissionViewSet, GroupViewSet


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('permissions', PermissionViewSet, basename='permissions')
router.register('groups', GroupViewSet, basename='groups')
urlpatterns = router.urls