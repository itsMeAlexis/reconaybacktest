from rest_framework.serializers import ModelSerializer

from contratos.models import Contrato


class ContratoSerializer(ModelSerializer):

    class Meta:
        model = Contrato
        fields = ['id', 'noContrato', 'tipoContrato', 'impMensualBruto', 'sueldoAnterior', 'fechaOficio', 'NoOficio', 'nombreSecretario', 'puestoSecretario', 'nombreSecretaria', 'nombreSolicitante', 'puestoSolicitante', 'nombreTestigo', 'puestoTestigo', 'nombreVobo', 'puestoVobo', 'domicilioSecretaria', 'nombrePdS', 'edadPdS', 'sexoPdS', 'estadoCivilPdS','curpdS', 'emailPdS', 'inePdS', 'domicilioPdS', 'cpPdS', 'rfcPdS', 'funcionesProf', 'tituloProf', 'institucionExpTituloProf', 'cedulaProf', 'statusFirma', 'statusCaptura', 'fechaCreacion', 'operativoProf', 'pdf1', 'pdf2', 'pdf3', 'pdf4', 'pdf5', 'pdf6', 'pdf7', 'pdf8','pdf9', 'dependencia_id', 'user_id', 'user_nombre','fechaInicioContrato' , 'fechaFinContrato', 'montoLetra', 'montoLetraAnterior' ,'telefonoPdS']
