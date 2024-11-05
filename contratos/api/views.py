from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#from django_filters.rest_framework import DjangoFilterBackend
#from django_filters import rest_framework as filters

from contratos.models import Contrato
from contratos.api.serializers import ContratoSerializer


class ContratoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ContratoSerializer
    queryset = Contrato.objects.all()
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['dependencia_id', 'user_id']

