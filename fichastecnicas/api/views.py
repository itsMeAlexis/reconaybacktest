
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from fichastecnicas.models import FichaTecnica
from fichastecnicas.api.serializers import FichaTecnicaSerializer

class FichaTecnicaApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FichaTecnicaSerializer
    queryset = FichaTecnica.objects.all()
    