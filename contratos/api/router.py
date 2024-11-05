from rest_framework.routers import DefaultRouter

from contratos.api.views import ContratoApiViewSet

router_contrato = DefaultRouter()

router_contrato.register(
    prefix = 'contratos', basename='contratos', viewset=ContratoApiViewSet
)