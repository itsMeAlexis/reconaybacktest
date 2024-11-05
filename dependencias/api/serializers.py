from rest_framework.serializers import ModelSerializer
from dependencias.models import Dependencia

class DependenciaSerializer(ModelSerializer):
    class Meta:
        model = Dependencia
        fields = ['id','nombreDependencia','DP', 'UR','nombreSecretario','puestoSecretario','nombreCoordinador','puestoCoordinador','NoUR','image','dependencia_id']
        