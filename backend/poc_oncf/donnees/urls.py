from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonneeViewSet,UpdateGeometriesView,EquipementSQLViewSet,ArcGISLayerAPI,AutoSyncView

router = DefaultRouter()
router.register(r'donnees', DonneeViewSet, basename='donnees')
router.register(r'auto-sync', AutoSyncView, basename='auto-sync')

urlpatterns = [
    path('api/', include(router.urls)),
    path('update-geometries/', UpdateGeometriesView.as_view(), name='update-geometries'),
    path('api/equipements/', EquipementSQLViewSet.as_view({'get': 'list'})),
    path('api/arcgis-layer/', ArcGISLayerAPI.as_view(), name='arcgis-layer'),

]
