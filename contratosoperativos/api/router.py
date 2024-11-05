from rest_framework.routers import DefaultRouter

from contratosoperativos.api.views import ContratoOperativoApiViewSet

router_contratooperativo = DefaultRouter()

router_contratooperativo.register(
    prefix = 'contratosoperativos', basename='contratosoperativos', viewset=ContratoOperativoApiViewSet
)