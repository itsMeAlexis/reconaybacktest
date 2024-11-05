from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#from django_filters.rest_framework import DjangoFilterBackend
#from django_filters import rest_framework as filters

from contratosoperativos.models import ContratoOperativo
from contratosoperativos.api.serializer import ContratoOperativoSerializer


class ContratoOperativoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ContratoOperativoSerializer
    queryset = ContratoOperativo.objects.all()
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['dependencia_id', 'user_id']

