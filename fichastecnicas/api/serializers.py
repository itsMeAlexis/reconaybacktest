from rest_framework.serializers import ModelSerializer

from fichastecnicas.models import FichaTecnica

class FichaTecnicaSerializer(ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = ['id','dependenciaFicha','nombrePdS','telefonoPdS','servicioRequerido','areaRequiereServicio','domicilioUnidadAdmin','nombreTitularSolicitante','cargoTitularSolicitante','tipoContrato','fechaInicioContrato','fechaFinContrato','importeMensual','ajusteMensual','nombreSecretario','puestoSecretario','nombreVoBo','puestoVoBo']