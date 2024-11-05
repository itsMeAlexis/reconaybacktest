from rest_framework.routers import DefaultRouter

from fichastecnicas.api.views import FichaTecnicaApiViewSet

router_fichatecnica = DefaultRouter()
router_fichatecnica.register(
    prefix='fichatecnica', basename='fichatecnica', viewset=FichaTecnicaApiViewSet
)