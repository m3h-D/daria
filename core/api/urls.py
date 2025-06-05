from django.urls import path
# from rest_framework.routers import DefaultRouter
from core.api.views import CoreViewSet

# router = DefaultRouter()

# router.register(r'', CoreViewSet, basename='core')

urlpatterns = [
    path('data/', CoreViewSet.as_view({'get': 'data'}), name='data'),
    path('rf_result/', CoreViewSet.as_view({'get': 'rf_result'}), name='rf_result'),
    path('y_result/', CoreViewSet.as_view({'get': 'y_result'}), name='y_result'),
]
