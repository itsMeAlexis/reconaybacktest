from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from dependencias.models import Dependencia
from dependencias.api.serializers import DependenciaSerializer

class DependenciaApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DependenciaSerializer
    queryset = Dependencia.objects.all()

