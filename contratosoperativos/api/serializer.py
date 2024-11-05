from rest_framework.serializers import ModelSerializer

from contratosoperativos.models import ContratoOperativo

class ContratoOperativoSerializer(ModelSerializer):
    class Meta:
        model = ContratoOperativo
        fields =['id', 'noContrato', 'tipoContrato', 'impMensualBruto', 'sueldoAnterior', 'fechaOficio', 'NoOficio', 'nombreSecretario', 'puestoSecretario', 'nombreSecretaria', 'nombreSolicitante', 'puestoSolicitante', 'nombreTestigo', 'puestoTestigo', 'nombreVobo', 'puestoVobo', 'domicilioSecretaria', 'nombrePdS', 'edadPdS', 'sexoPdS', 'estadoCivilPdS','curpdS', 'emailPdS', 'inePdS', 'domicilioPdS', 'cpPdS', 'rfcPdS', 'statusFirma', 'statusCaptura', 'fechaCreacion', 'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8', 'dependencia_id', 'user_id','user_nombre','funcionesPsD','fechaInicioContrato','fechaFinContrato','montoLetra', 'montoLetraAnterior' ,'telefonoPdS']
