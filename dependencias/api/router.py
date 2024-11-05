from rest_framework.routers import DefaultRouter
from dependencias.api.views import DependenciaApiViewSet

router_dependencia = DefaultRouter()

router_dependencia.register(
    prefix='dependencias', basename='dependencias', viewset=DependenciaApiViewSet
)