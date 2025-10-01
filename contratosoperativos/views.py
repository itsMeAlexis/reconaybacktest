from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, PageTemplate, Frame, PageBreak, KeepInFrame, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from .models import ContratoOperativo
from contratosoperativos.models import ContratoOperativo
import locale
import datetime
import os


class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page = "Pagina %s de %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(195*mm, 262*mm, page)

def create_content(paragraphs, max_lines_per_page=40):
    styles = getSampleStyleSheet()
    content = []
    lines_count = 0

    for paragraph in paragraphs:
        lines = paragraph.count("<br/>") + 1  # Contar las líneas en el párrafo
        if lines_count + lines <= max_lines_per_page:
            p = Paragraph(paragraph, styles['Normal'])
            content.append(p)
            lines_count += lines
        else:
            break

    return content


def generate_PDF_Operativo(request, contratoOperativo_id):
    contratoOperativo = get_object_or_404(ContratoOperativo, id=contratoOperativo_id)

    right_aligned_style = ParagraphStyle(
        'Center',
        fontSize=10,
        leading=12,
        alignment=TA_RIGHT,
        fontName='Helvetica'
    )

      # Crear estilos personalizados
    styles = getSampleStyleSheet()

    # Función para aplicar estilos a los párrafos
    
    def apply_style(para, styles):
        formatted_elements = []
        for style_name in styles:
            style = custom_styles.get(style_name, None)
            if style:
                if style_name == "space":
                    # Si el estilo es "space", llamamos a la función y le pasamos el tamaño de espacio (en puntos)
                    formatted_elements.append(style(12))  # Aquí 12 es el tamaño de espacio deseado
                else:
                    formatted_elements.append(Paragraph(para, style))
        return formatted_elements
    
    custom_styles = {
        "bold": ParagraphStyle(name="Bold", fontName="Helvetica-Bold", fontSize=12),
        "underline": ParagraphStyle(name="Underline", fontName="Helvetica", fontSize=12, textColor="blue", spaceAfter=10),
        "normal": ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=12),
        "centered": ParagraphStyle(name="Centered", fontName="Helvetica", fontSize=12, alignment=1),
        "justify": ParagraphStyle(name="Justify", fontName="Helvetica", fontSize=12, alignment=TA_JUSTIFY),
        "right": ParagraphStyle(name="Right", fontName="Helvetica", fontSize=12, alignment=2),
        "space": lambda size: Spacer(1, size),  # Agregar función para el estilo "space"

    }

    # Establecer la configuración regional en español
    #locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

    # Define la fecha
    fecha_inicio_contrato = contratoOperativo.fechaInicioContrato
    fecha_fin_contrato = contratoOperativo.fechaFinContrato

    # Convierte la fecha en un objeto datetime
    fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio_contrato, "%Y-%m-%d")
    fecha_fin_obj = datetime.datetime.strptime(fecha_fin_contrato, "%Y-%m-%d")

    nombres_meses_espanol = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    # Obtén el nombre del mes
    #nombre_mes_inicio = fecha_inicio_obj.strftime("%B")
    #nombre_mes_fin = fecha_fin_obj.strftime("%B")
    nombre_mes_inicio = nombres_meses_espanol[fecha_inicio_obj.month-1]
    nombre_mes_fin = nombres_meses_espanol[fecha_fin_obj.month-1]
                    
             
    # Formatea la fecha en el formato deseado
    fecha_formateada_inicio = fecha_inicio_obj.strftime("%d de {} de %Y").format(nombre_mes_inicio)
    fecha_formateada_fin = fecha_fin_obj.strftime("%d de {} de %Y").format(nombre_mes_fin)

    #fecha_formateada_inicio = 'fechaInicio'
    #fecha_formateada_fin = 'fechaFin'
    # Estilo del párrafo
    #style = ParagraphStyle(
       # "custom",
        #alignment=TA_CENTER,
       # fontSize=12,
    #)

    #locale.setlocale(locale.LC_ALL, 'es-MX')

    no_contrato = contratoOperativo.noContrato if contratoOperativo.noContrato is not None else "&nbsp"

    nombre_secretario_solicitante =  contratoOperativo.nombreSolicitante if contratoOperativo.nombreSecretaria == "SECRETARIA DE ADMINISTRACION Y FINANZA" or contratoOperativo.nombreSecretaria == "Secretaría de Administración y Finanzas" or contratoOperativo.nombreSecretaria == "SECRETARÍA DE ADMINISTRACIÓN Y FINANZA" or contratoOperativo.nombreSecretaria == "Secretaria de Administracion y Finanzas" or contratoOperativo.nombreSecretaria == "Secretaría de Administracion y Finanzas" or contratoOperativo.nombreSecretaria == "Secretaria de Administración y Finanzas" or contratoOperativo.nombreSecretaria == "SECRETARÍA DE ADMINISTRACION Y FINANZA" or contratoOperativo.nombreSecretaria == "SECRETARIA DE ADMINISTRACIÓN Y FINANZA"  else contratoOperativo.nombreSecretario

   # nombre_secretario_solicitante =  "si" if contratoOperativo.nombreSecretaria == "SECRETARÍA DE MOVILIDAD" or contratoOperativo.nombreSecretaria == "Secretaria de Movilidad" else "no"

    puesto_secretario_solicitante =  contratoOperativo.puestoSolicitante if contratoOperativo.nombreSecretaria == "SECRETARIA DE ADMINISTRACION Y FINANZAS" or contratoOperativo.nombreSecretaria == "Secretaría de Administración y Finanzas" else contratoOperativo.puestoSecretario

    #no_cedula = contrato.cedulaProf if contrato.cedulaProf is not None else "N/A"

    #Usando operador ternario para tituloProf
    #titulo_profesional = contrato.tituloProf.upper() if contrato.tituloProf else "Título no especificado"

    # Usando operador ternario para cedulaProf
    #cedula_profesional = contratoOperativo.cedulaProf.upper() if contratoOperativo.cedulaProf else "N/A"

    paragraphs =[   
        
        "<para align='right'><b>CONTRATO No:</b><b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></b></para>".format(no_contrato),

        "<para>&nbsp;</para>",
        
        "<para align='right'><b>IMPORTE MENSUAL BRUTO $:</b><b><u>&nbsp;&nbsp;&nbsp;&nbsp;" +   "{:,.2f}".format(contratoOperativo.impMensualBruto) + "&nbsp;&nbsp;&nbsp;&nbsp;</u></b></para>",
        
        "<para>&nbsp;</para>",
          
        "<para align='justify'><b>CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES SUJETO AL PAGO DE HONORARIOS BAJO EL RÉGIMEN FISCAL DE INGRESOS ASIMILADOS A SALARIOS, POR TIEMPO DETERMINADO,</b> QUE CELEBRAN POR UNA PARTE, EL PODER EJECUTIVO DEL ESTADO DE NAYARIT A TRAVÉS DE LA SECRETARÍA DE ADMINISTRACIÓN Y FINANZAS, REPRESENTADA EN ESTE ACTO POR EL <b>DIRECTOR GENERAL DE ADMINISTRACIÓN, LIC JUAN ALBERTO PINEDA CISNEROS</b>, A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ “<b>LA DEPENDENCIA</b>” Y POR LA OTRA PARTE, EL(A) C. <u>&nbsp;&nbsp;" + contratoOperativo.nombrePdS.upper() + "&nbsp;&nbsp;</u>, EN LO SUCESIVO “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, A QUIENES AL ACTUAR EN CONJUNTO SE LES DENOMINARÁ “<b>LAS PARTES</b>” AL TENOR DE LOS ANTECEDENTES, DECLARACIONES Y CLÁUSULAS SIGUIENTES:</para>",
        
        "<para>&nbsp;</para>",

        "<para align='center'><b>ANTECEDENTES</b></para>",
         
        "<para>&nbsp;</para>",

        "<para align='justify'>Que en fecha <u>&nbsp;&nbsp; " + contratoOperativo.fechaOficio.upper() + "&nbsp;&nbsp;</u>, mediante Oficio No. <u>&nbsp;&nbsp;" + contratoOperativo.NoOficio.upper() + "&nbsp;&nbsp;</u>, firmado por el(a) <u>&nbsp;&nbsp;"+ nombre_secretario_solicitante +"&nbsp;&nbsp;</u>, en su carácter de <u>&nbsp;&nbsp;"+ puesto_secretario_solicitante + "&nbsp;&nbsp;</u>, solicitó al SECRETARIO DE ADMINISTRACION Y FINANZAS DEL PODER EJECUTIVO DEL ESTADO DE NAYARIT, <b>MTRO. EN FISCAL JULIO CESAR LÓPEZ RUELAS</b>, que con cargo al Presupuesto del(a) <u>&nbsp;&nbsp; " + contratoOperativo.nombreSecretaria.upper() + "&nbsp;&nbsp;</u>, celebrara Contrato Civil de Prestación de Servicios Profesionales sujeto al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por tiempo determinado, con el(a) C.<u>&nbsp;&nbsp;" + contratoOperativo.nombrePdS.upper() + "&nbsp;&nbsp;</u>, para que a partir del día&nbsp; " + fecha_formateada_inicio + ", preste los servicios profesionales que se describen en la Cláusula PRIMERA de este instrumento, el cual se encuentra debidamente autorizado por el Titular del Poder Ejecutivo, en términos del documento que se adjunta.</para>".format(nombre_secretario_solicitante),
         
        "<para>&nbsp;</para>",
    
        "<para align='center'><b>DECLARACIONES</b></para>",

        "<para>&nbsp;</para>",
    
        "<b>1.- DECLARA “LA DEPENDENCIA”, A TRAVÉS DE SU REPRESENTANTE, QUE:</b>",

        "<para>&nbsp;</para>",
   
        "<para align='justify'><b>1.1- </b>La Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, forma parte de la Administración Pública Centralizada del Gobierno del Estado de Nayarit, de conformidad con lo establecido en el artículo 72 de la Constitución Política del Estado Libre y Soberano de Nayarit, y los artículos 1 y 31 fracción II de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit; y tiene entre sus atribuciones el coordinar la planeación y aplicación de la política administrativa, financiera, crediticia, fiscal, hacendaria y del gasto público de la Administración Pública Estatal, además de normar y regular la prestación de servicios administrativos que requieran las Dependencias; lo anterior, con fundamento en lo dispuesto en el artículo 33 de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>1.2.-</b> Su representante, el Director General de Administración de la Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, participa en la celebración del presente instrumento con fundamento en los artículos 19 y 26 de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit, y los artículos 9, fracción VII, y 67 fracción XIV, del Reglamento Interior de la Secretaría de Administración y Finanzas, y demás normativa aplicable; quien acredita su personalidad con el nombramiento expedido a su favor por el Titular de la Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, Mtro. en Fiscal Julio César López Ruelas, de fecha 16 de febrero de 2023.</para>",
       
        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.3.-</b> Su representada está inscrita en el Registro Federal de Contribuyentes con la clave SAD091223KK7, con domicilio fiscal sito en Avenida México sin número, Centro, Tepic Nayarit, C.P. 63000, mismo que señala para todos los efectos que se derivan del presente contrato.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>1.4.-</b> De acuerdo a las necesidades propias de “<b>LA DEPENDENCIA</b>”, se requiere temporalmente la contratación de los servicios de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, para llevar a cabo las acciones materia de este contrato.</para> ",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>1.5.-</b> Cuenta con la disponibilidad presupuestal para el pago de los servicios requeridos, motivo del presente contrato, afectando la partida presupuestal número 12101 del Presupuesto de Egresos del Estado Libre y Soberano de Nayarit para el Ejercicio Fiscal 2024.</para>",

        "<para>&nbsp;</para>",

        "<b>2.- DECLARA “EL(A) PRESTADOR(A) DE SERVICIOS”, QUE:</b>",

        "<para>&nbsp;</para>",
   
        "<para align='justify'><b>2.1.-</b> Tiene la capacidad jurídica para contratar y obligarse en los términos del presente instrumento civil, y que cuenta con los conocimientos profesionales y la experiencia necesaria para prestar los servicios que requiere “<b>LA DEPENDENCIA</b>”.</para>",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>2.2.-</b> Es una persona física de nacionalidad mexicana, de <u>&nbsp;&nbsp;" + contratoOperativo.edadPdS.upper() + "&nbsp;&nbsp;</u> años, sexo <u>&nbsp;&nbsp; " + contratoOperativo.sexoPdS.upper() +"&nbsp;&nbsp;</u>, estado civil<u>&nbsp;&nbsp; " + contratoOperativo.estadoCivilPdS.upper() + "&nbsp;&nbsp;</u>, C.U.R.P.<u>&nbsp;&nbsp;" + contratoOperativo.curpdS.upper() +"&nbsp;&nbsp;</u>, correo electrónico<u>&nbsp;&nbsp; " +contratoOperativo.emailPdS.upper() +" &nbsp;&nbsp;</u>; credencial para votar vigente, con clave <u>&nbsp;&nbsp; " + contratoOperativo.inePdS.upper() +"&nbsp;&nbsp;</u> y que su domicilio particular para los efectos legales de este contrato es el ubicado en <u>&nbsp;&nbsp; " + contratoOperativo.domicilioPdS.upper() +"&nbsp;&nbsp;</u>C.P.<u>&nbsp;&nbsp; " + contratoOperativo.cpPdS.upper() +"&nbsp;&nbsp;</u>.</para>",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>2.3.-</b> Está inscrita(o) en el Registro Federal de Contribuyentes, bajo el número <u>&nbsp;&nbsp;" + contratoOperativo.rfcPdS.upper() + "&nbsp;&nbsp;</u>, y está al corriente del cumplimiento de sus obligaciones fiscales, tal y como lo acredita con constancia de situación fiscal actualizada. </para>",

        "<para>&nbsp;</para>",
      
        "<para align='justify'><b>2.4.-</b> Ha sido su voluntad ofrecer a “<b>LA DEPENDENCIA</b>” los servicios objeto del presente contrato, bajo el régimen fiscal de honorarios asimilados a salarios y por tiempo determinado, empleando todos sus conocimientos, capacidades técnicas y tiempo que sea necesario para el cabal cumplimiento del presente contrato.</para>",

        "<para align='justify'><b>2.5.-</b>Es una persona física ajena a “<b>LA DEPENDENCIA</b>” por lo que puede denominársele el(la) “<b>PRESTADOR(A) DE SERVICIOS</b>”, que presta sus servicios de manera independiente a toda persona física o moral que le solicite la prestación de sus servicios y que su actividad profesional no la presta preponderantemente a “<b>LA DEPENDENCIA</b>”.</para> ",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>2.6.-</b>La prestación de los servicios  a los que se refiere este contrato es de naturaleza civil, sujeta al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por tiempo determinado, que se encuentra regulada por el Título IV, Capítulo II, de la Ley del Impuesto sobre la Renta vigente.</para>",

        "<para>&nbsp;</para>",
     
        "<para align='justify'><b>2.7.-</b> Se obliga a someterse a los términos del presente contrato de prestación de servicios profesionales de naturaleza civil, en virtud de que este instrumento no se considera en ningún momento contrato laboral. Por ello “<b>LA DEPENDENCIA</b>”, no será patrón directo ni indirecto, y no contrae obligación, ni responsabilidad alguna al respecto.</para>",
        
        "<para>&nbsp;</para>",
  
        "<para align='justify'><b>2.8.-</b> Manifiesta su conformidad para que “<b>LA DEPENDENCIA</b>” realice los descuentos a los honorarios que por el presente contrato se generen y se realicen los pagos correspondientes ante las autoridades hacendarias, conforme a lo dispuesto en el artículo 94 fracción IV de la Ley del Impuesto sobre la Renta, para los efectos fiscales a que haya lugar.</para>",

        "<para>&nbsp;</para>",

        "<b>3.- AMBAS PARTES DECLARAN, QUE:</b>",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>3.1.-</b> Se reconocen mutuamente la personalidad con la que se ostentan, por lo que desde este momento se obligan a no objetar ni revocar en lo futuro por ninguna causa esta condición y, por consiguiente, no podrán alegar posteriormente la nulidad de los actos aquí establecidos por dicho concepto.</para>",

        "<para>&nbsp;</para>",
     
        "<para align='justify'><b>3.2.-</b> Expresan su voluntad para la celebración del presente contrato, reconociendo y aceptando que el mismo se rige por lo dispuesto en los artículos 1165, 1166, 1168, 1169, 1212, 1224, 1977, 1986 y demás relativos y aplicables del Código Civil para el Estado de Nayarit.</para> ",

        "<para>&nbsp;</para>",
  
        "<para align='justify'><b>3.3.-</b> Haber negociado libremente de toda coacción los términos de este documento, que no existe ninguna limitante a su intención o voluntad y consecuentemente se encuentra con capacidad y aptitud legal para celebrar el presente contrato.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>3.4.-</b> Manifiestan “<b>LAS PARTES</b>” que están de acuerdo con las declaraciones anteriores y siendo su deseo obligarse recíprocamente, ambas partes acuerdan sujetarse al tenor de las siguientes:</para>",

        "<para>&nbsp;</para>",
  
        "<para align='center'><b>CLÁUSULAS</b></para>",

        "<para>&nbsp;</para>",
   
        "<b>PRIMERA.-</b> OBJETO DEL CONTRATO.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” por virtud del presente instrumento, se obliga civilmente a prestar a “<b>LA DEPENDENCIA</b>”, sus servicios, con el objeto de realizar funciones de ayudantía, brindando apoyo en diversas cuestiones de índole personal, manteniendo limpias sus instalaciones y demás que durante la vigencia del presente contrato se le asignen.</para>",

        "<para>&nbsp;</para>",
      
        "<b>SEGUNDA.-</b> CONDICIONES GENERALES.",

        "<para>&nbsp;</para>",
        
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” se obliga a prestar los servicios señalados en la Cláusula inmediata anterior, con toda diligencia, obligándose a aportar toda su experiencia y capacidad, dedicando todo el tiempo que considere necesario para dar cabal cumplimiento al presente contrato, ello sin estar sujeta a un horario, dada la especial naturaleza del presente contrato, pudiendo “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” realizar sus tareas en los tiempos y formas que estime pertinentes. Estando “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, no obstante la vigencia del presente contrato, en plena libertad de ofertar sus servicios profesionales a otros entes públicos o privados.</para> ",

        "<para>&nbsp;</para>",
       
        "<para align='justify'>Toda la información que obtenga “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” de “<b>LA DEPENDENCIA</b>”, y viceversa, será manejada en forma confidencial y sólo podrá ser usada para cumplir con los fines del presente contrato.</para> ",

        "<para>&nbsp;</para>",
       
        "<b>TERCERA.-</b> IMPORTE DEL CONTRATO.",

        "<para>&nbsp;</para>",

        "<para align='justify'>“<b>LA DEPENDENCIA</b>” se obliga a cubrir por concepto de honorarios a “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” por la prestación de Servicios sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, a que se refiere este contrato, la cantidad de <u>&nbsp;&nbsp;&nbsp;&nbsp;" + "{:,.2f}".format(contratoOperativo.impMensualBruto) + "&nbsp;&nbsp;&nbsp;&nbsp;</u> cantidad con letra <u>&nbsp;&nbsp;" + contratoOperativo.montoLetra.upper() + "&nbsp;&nbsp;</u>  mensuales, que podrá ser distribuida en percepciones quincenales, efectuando la retención del Impuesto Sobre la Renta correspondiente en términos de los artículos 94 fracción IV y 96 de la Ley del Impuesto Sobre la Renta y demás correlativos aplicables.</para> ",

        "<para>&nbsp;</para>",
       
        "<para align='justify'>Los pagos se harán “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” mediante dispersión electrónica en una cuenta bancaria personal, tramitada para tal efecto por la Dirección de Pago Electrónico de Servicios Personales de la Dirección General de Tesorería de la Secretaría de Administración y Finanzas.</para>",

        "<para>&nbsp;</para>",
        
        "<para align='justify'>Queda bajo la responsabilidad de la Unidad Administrativa solicitante informar a la Secretaría de Administración y Finanzas de cualquier movimiento que se realice con motivo del presente contrato, así como del cumplimiento o incumplimiento por parte de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”.</para>",

        "<para>&nbsp;</para>",
       
        "<b>CUARTA.-</b> VIGENCIA DEL CONTRATO.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>El presente contrato civil tendrá una vigencia improrrogable del día &nbsp; " + fecha_formateada_inicio + " &nbsp y hasta el &nbsp; " + fecha_formateada_fin + ". Concluida la vigencia no podrá haber prórroga automática por el simple transcurso del tiempo y terminará sin necesidad de darse aviso entre “<b>LAS PARTES</b>”. Para el caso de que “<b>LA DEPENDENCIA</b>” tuviera necesidad de contar nuevamente con los servicios de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, se requerirá la celebración de un nuevo contrato.</para>",

        "<para>&nbsp;</para>",
        
        "<b>QUINTA.-</b> VIGILANCIA.",

        "<para>&nbsp;</para>",

        "<para align='justify'>“<b>LA DEPENDENCIA</b>” a través de los representantes que para tal efecto designe, tendrá en todo tiempo el derecho de vigilar el estricto cumplimiento de este contrato civil, por lo que podrá revisar e inspeccionar las actividades desempeñadas por “<b>LA PRESTADORA DE SERVICIOS</b>”.</para>",

        "<para>&nbsp;</para>",
  
        "<b>SEXTA.-</b> NATURALEZA DE LA RELACIÓN. ",

        "<para>&nbsp;</para>",
   
        "<para align='justify'>“<b>LAS PARTES</b>” quedan liberadas de otorgarse prestaciones propias de una relación de trabajo, por estar frente a un contrato de prestación de servicios profesionales de naturaleza civil.</para>",

        "<para>&nbsp;</para>",
       
        "<b>SÉPTIMA.-</b> INFORMES DE LOS SERVICIOS.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” mantendrá informada verbalmente o por escrito en el caso de así habérselo solicitado a la requirente de servicio, por conducto del titular del área solicitante, del estado que guardan las actividades materia del presente contrato.</para>",

        "<para>&nbsp;</para>",
       
        "<b>OCTAVA.-</b> IMPEDIMENTO.",

        "<para>&nbsp;</para>",
   
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” no podrá, en ningún momento y por ninguna razón, ceder o subrogar los derechos y obligaciones derivados del presente instrumento a terceras personas físicas y/o morales.</para>",

        "<para>&nbsp;</para>",
  
        "<b>NOVENA.-</b> MODIFICACIONES.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>Cualquier variación en lo pactado en este contrato de prestación de servicios profesionales, será acordada por “<b>LAS PARTES</b>” en forma previa y escrita, celebrando para ello el convenio modificatorio correspondiente, debiendo,para su validez, estar firmado por ambas partes, señalarse claramente que se trata de una modificación, y se determine su alcance. En el entendido de que cualquier convenio verbal es y será nulo.</para> ",

        "<para>&nbsp;</para>",
     
        "<b>DÉCIMA.- “EL(A) PRESTADOR(A) DE SERVICIOS</b>”, SE COMPROMETE A LO SIGUIENTE: ",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>a) No divulgar ni dar a conocer los datos y documentos que “<b>LA DEPENDENCIA</b>” le proporcione para las actividades que desarrolla, ni dar informes a personas distintas a las señaladas por ella.</para>",
    
        "<para>&nbsp;</para>",

        "<para align='justify'>b) Ser directamente responsable de los daños y perjuicios que cause a “<b>LA DEPENDENCIA</b>” y/o a terceros, por negligencia, impericia, omisión o dolo en la prestación de los servicios que se obliga a realizar.</para> ",

        "<para>&nbsp;</para>",

        "<b>DÉCIMA PRIMERA.-</b>INFORMACIÓN GENERADA.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” manifiesta estar enterado de que todos los archivos, documentación y/o información que genere al prestar sus servicios profesionales independientes a “<b>LA DEPENDENCIA</b>” será propiedad de la segunda, y por ningún motivo podrá disponer de ella para asuntos y/o situaciones distintas a la prestación de sus servicios, y en todo caso, una vez finalizada la contraprestación de los mismos, no podrá utilizar ni reproducir archivos, documentación y/o información alguna; así mismo, al tratarse de propiedad de “<b>LA DEPENDENCIA</b>”, “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” no podrá eliminar física ni digitalmente tales archivos, documentación y/o información.</para>",

        "<para>&nbsp;</para>",
        
        "<b>DÉCIMA SEGUNDA.-</b>TERMINACIÓN ANTICIPADA.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>LA DEPENDENCIA</b>”, en cualquier momento, podrá dar por terminado anticipadamente el presente contrato sin responsabilidades para ésta y sin necesidad de que medie resolución judicial alguna, dando aviso por escrito a “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” con al menos 15 (quince) días naturales de anticipación. Asimismo “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” podrá darlo por concluido de manera anticipada, previo aviso por escrito a “<b>LA DEPENDENCIA</b>”, en un lapso no menor a 15 (quince) días hábiles.</para>",

        "<para>&nbsp;</para>",
      
        "<para align='justify'>“<b>LA DEPENDENCIA</b>” solo adquiere y reconoce las obligaciones derivadas de la legislación aplicable al presente contrato de naturaleza meramente civil.</para>",

        "<para>&nbsp;</para>",
        
        "<b>DÉCIMA TERCERA.-</b>CASO FORTUITO O FUERZA MAYOR.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, no será responsable por cualquier evento de caso fortuito o de fuerza mayor que le impidiera parcial o totalmente la ejecución de las obligaciones a su cargo en el presente contrato, en el entendido de que el caso fortuito o fuerza mayor, según corresponda, estén debidamente acreditados.</para>",

        "<para>&nbsp;</para>",
       
        "<b>DÉCIMA CUARTA.-</b>INTERPRETACIÓN Y JURISDICCIÓN.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>Los títulos de las cláusulas que aparecen en el presente contrato, se han plasmado con el exclusivo propósito de facilitar su lectura, por tanto, no definen ni limitan el contenido de las mismas. Para efectos de interpretación de cada cláusula deberá atenderse exclusivamente a su contenido y de ninguna manera a su título.</para>",

        "<para>&nbsp;</para>",
      
        "<para align='justify'>Para la interpretación y cumplimiento del presente contrato, “<b>LAS PARTES</b>” se someten a la jurisdicción y competencia de los Juzgados Civiles de la ciudad de Tepic, Nayarit, así como a las disposiciones contenidas en el Código Civil para el Estado de Nayarit vigente, renunciando expresamente al fuero que pudiera corresponderles en razón de su domicilio actual o futuro.</para> ",

        "<para>&nbsp;</para>",

        "<para align='justify'><b>DÉCIMA QUINTA</b>.- Queda expresamente convenido que la falta de cumplimiento a cualquiera de las obligaciones que aquí se contraen y aquellas otras que dimanan del Código Civil para el Estado de Nayarit vigente, será motivo de rescisión del presente contrato y derivará además en el pago de los daños y perjuicios que el incumplimiento cause a la parte que cumple.</para>",

        "<para>&nbsp;</para>",
   
        "<para align='justify'><b>DÉCIMA SEXTA</b>.- “<b>LAS PARTES</b>” quedan obligadas a dar cumplimiento a las cláusulas del presente instrumento jurídico sujetándose a lo dispuesto por el Código Civil para el Estado de Nayarit, por tratarse de un contrato de prestación de servicios profesionales sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por consiguiente, quedan liberadas de otorgarse prestaciones propias de una relación de trabajo, por lo que “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” releva a “<b>LA DEPENDENCIA</b>” de cualquier responsabilidad presente o futura por este concepto.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>DÉCIMA SÉPTIMA</b>.- En razón del correcto y cabal cumplimiento del presente contrato por parte de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, “<b>LA DEPENDENCIA</b>” tendrá total independencia para considerar entregarle un bono de gratificación, que podría otorgarse por un monto equivalente de hasta dos meses, respecto a lo señalado en la Cláusula TERCERA, indistintamente del período del término del contrato, siempre y cuando se cuente con la disponibilidad presupuestal en el ejercicio fiscal de que se trate, y a discrecionalidad de “<b>LA DEPENDENCIA</b>”, por tal motivo, no constituye una obligación para “<b>LA DEPENDENCIA</b>”.</para>",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>Leído que fue el presente contrato y enteradas las partes del contenido y alcance de todas y cada una de sus cláusulas, lo firman por duplicado, ante los testigos que al final suscriben, en la Ciudad de Tepic, Nayarit, el día &nbsp; " + fecha_formateada_inicio + ".</para>",
        
        
        "<para>&nbsp;</para>",
        "<para>&nbsp;</para>",
        "<para>&nbsp;</para>",
        

    ]

    styles_to_apply = [
    "bold",      # Negritas
    "underline", # Subrayado
    "normal",    # Párrafo normal
    "space",     # Espacio (salto de línea)
    "center",  # Centrado
    "justify",   # Justificado
    "right",     # Alineado a la derecha
    ]   
    
     # Lista para almacenar los párrafos formateados
    formatted_paragraphs = []
    #all_elements = []
    # Aplicar estilos a cada párrafo y agregarlos a la lista
    for para in paragraphs:
        elements = apply_style(para, styles_to_apply)
        formatted_paragraphs.extend(elements)

    content = []

    centered_style_2 = ParagraphStyle(
        'Normal',
        fontSize=9,
        parent=styles['Normal'],
        alignment=TA_CENTER,
    )

    # Estilo personalizado con alineación centrada
    centered_style = ParagraphStyle(
        'Center',
        parent=styles['Normal'],
        alignment=TA_CENTER,
    )

    centered_style_2 = ParagraphStyle(
        'Center',
        fontSize=9,
        parent=styles['Normal'],
        alignment=TA_CENTER,
    )

    # Estilo personalizado para los encabezados del documento
    header_style = ParagraphStyle(
        'Header',
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    data = [
            [Paragraph("<b> POR “LA DEPENDENCIA” </b>", centered_style),
            Paragraph(""),
            Paragraph("<b> “EL (A) PRESTADOR(A) DEL SERVICIO” </b>", centered_style)],
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style),],         
            [Paragraph("<b>LIC. JUAN ALBERTO PINEDA CISNEROS</b> <br/> DIRECTOR GENERAL DE ADMINISTRACIÓN DE  LA SECRETARÍA DE ADMINISTRACIÓN Y FINANZAS DEL PODER EJECUTIVO DEL ESTADO DE NAYARIT.", centered_style_2),
            Paragraph(""),
            Paragraph("<b>" + f"&nbsp;&nbsp;{contratoOperativo.nombrePdS.upper()}&nbsp;&nbsp;" + " </b>", centered_style)],
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style),],         
            [Paragraph("<b>ÁREA SOLICITANTE</b>", centered_style),
            Paragraph(""),
            Paragraph("<b>TESTIGO</b>", centered_style)],         
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style)],
            [Paragraph("<b>" + f"&nbsp;&nbsp;{contratoOperativo.nombreSolicitante.upper()}&nbsp;&nbsp;" + " </b>", centered_style),
            Paragraph(""),
            Paragraph("<b>" + f"&nbsp;&nbsp;{contratoOperativo.nombreTestigo.upper()}&nbsp;&nbsp;" + "</b>", centered_style)],               
            [Paragraph(f"&nbsp;&nbsp;{contratoOperativo.puestoSolicitante.upper()}&nbsp;&nbsp;", centered_style_2),
            Paragraph(""),
            Paragraph(f"&nbsp;&nbsp;{contratoOperativo.puestoTestigo.upper()}&nbsp;&nbsp;", centered_style_2),
            ],
             
        ]    

    # Crear la tabla y especificar el estilo para el contenido de la tabla
    table = Table(data, colWidths=[210, 50, 210], style=[
        ('GRID', (0, 0), (-1, -1), 1, colors.white),  # Agregar bordes a todas las celdas
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el contenido al centro de las celdas horizontalmente
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinear el contenido al centro de las celdas verticalmente
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Especificar la fuente en negrita (Helvetica-Bold)
        #('LINEBELOW', (0, 0), (0, 0), 1, colors.black),  # Subrayar solo la primera fila
        ('LINEBELOW', (0, 1), (0, 1), 1, colors.black),  # Subrayar solo la primera celda de la segunda fila (parte inferior)
        ('LINEBELOW', (2, 1), (2, 1), 1, colors.black),  # Subrayar solo la segunda celda de la segunda fila (parte inferior)
        ('LINEBELOW', (0, 5), (0, 5), 1, colors.black),  # Subrayar solo la primera celda de la cuarta fila (parte inferior)
        ('LINEBELOW', (2, 5), (2, 5), 1, colors.black),  # Subrayar solo la segunda celda de la cuarta fila (parte inferior)
    
    ])

   

    buffer = BytesIO()
    top_margin = 70  # Ajustar según tus preferencias
    bottom_margin = 70  # Ajustar según tus preferencias
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=top_margin, bottomMargin=bottom_margin)

    # Definir un marco que cubra toda la página
    page_width, page_height = letter
    frame = Frame(0, 0, page_width, page_height, id='normal', leftPadding=72, rightPadding=72,
                  topPadding=top_margin, bottomPadding=bottom_margin)

    # Crear el PageTemplate con el marco definido
    page_template = PageTemplate(id='main', frames=[frame], onPage=header_footer)

    # Agregar el PageTemplate al SimpleDocTemplate
    doc.addPageTemplates([page_template])

    #styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    # Creamos un estilo personalizado para el párrafo alineado a la derecha
    right_aligned_style = ParagraphStyle('RightAligned', parent=styles['Normal'], alignment=2)
    center_aligned_style = ParagraphStyle('RightAligned', parent=styles['Normal'], alignment=TA_CENTER)
    left_aligned_style = ParagraphStyle('RightAligned', parent=styles['Normal'], alignment=TA_LEFT)
    justify_aligned_style = ParagraphStyle('RightAligned', parent=styles['Normal'], alignment=4)
 
    
    # Definir un marco que cubra toda la página
    leftMargin, bottomMargin, width, height = 72, 18, 468, 756
    frame = Frame(leftMargin, bottomMargin, width, height, id='normal')

    page_num = 1
    while paragraphs:
        content_page = create_content(paragraphs)
        content += content_page
        paragraphs = paragraphs[len(content_page):]
        if paragraphs:
            content.append(Spacer(1, 12))  # Agregar un espacio entre páginas
        page_num += 1

    content.append(table)
    
    page_template = PageTemplate(id='main', frames=[frame], onPage=header_footer)  #agregue
    #content = [formatted_paragraphs]  # Agregar formatted_parrafo a la lista content
    doc.build(content, canvasmaker=PageNumCanvas)
    #doc.build(canvasmaker=PageNumCanvas)
        

    # Obtener el contenido del buffer y crear una respuesta HTTP con el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = f'attachment; filename="contrato_{contratoOperativo_id}.pdf"'
    response.write(pdf)
    
    

    return response

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_width, page_height = letter
    canvas.restoreState()    
    # Lista para almacenar el contenido del contrato


#### INICIO DEL REPORTE DE SECRETARIA DE FINANZAS ####

def generate_PDF_OperativoFIN(request, contratoOperativo_id):
    contratoOperativo = get_object_or_404(ContratoOperativo, id=contratoOperativo_id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # Crear estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilos
    title_style = ParagraphStyle(
        'Title',
        fontSize=10,
        leading=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=3
    )
    
    field_label_style = ParagraphStyle(
        'FieldLabel',
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leftIndent=0
    )
    field_label_style_center = ParagraphStyle(
        'FieldLabel',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leftIndent=0
    )
    
    field_value_style = ParagraphStyle(
        'FieldValue',
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leftIndent=0,
        borderWidth=1,
        borderColor=colors.black,
        borderPadding=5
        
    )

    field_value_style_center = ParagraphStyle(
        'FieldValue',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leftIndent=0,
        borderWidth=1,
        borderColor=colors.black,
        borderPadding=5
        
    )
    
    # Construir la ruta absoluta de la imagen
    imagen_path = os.path.join(os.path.dirname(__file__), 'finanzas.jpg')
    
    # Crear contenido del documento
    content = []
    
    # Encabezado con logo y títulos
    header_data = [
        [Image(imagen_path, width=3*inch, height=2*inch, kind='proportional')],
        [Paragraph("FICHA TÉCNICA DE VALIDACIÓN", title_style)],
        [Paragraph("CONTRATOS DE PRESTACIÓN DE SERVICIOS PROFESIONALES SUJETOS AL PAGO DE HONORARIOS<br/>BAJO EL RÉGIMEN FISCAL DE INGRESOS ASIMILADOS A SALARIOS 1er SEMESTRE 2025", subtitle_style)],
    ]
    
    header_table = Table(header_data)
    header_table.setStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 0), (2, 0), 'CENTER'),
    ])
    
    content.append(header_table)
    content.append(Spacer(1, 20))
    #imprimir contrato
    # Imprimir todos los campos del contrato dinámicamente
    print("=== DATOS DEL CONTRATO OPERATIVO ===")
    for field in contratoOperativo._meta.get_fields():
        field_name = field.name
        try:
            field_value = getattr(contratoOperativo, field_name)
            print(f"{field_name}: {field_value}")
        except AttributeError:
            print(f"{field_name}: [Campo no accesible]")
    # Fin imprimir contrato

    # Sección de DEPENDENCIA y CONTRATO No.
    no_contrato = contratoOperativo.noContrato if contratoOperativo.noContrato else "\u00A0"
    form_data_dependencia_contrato = [
        # DEPENDENCIA y CONTRATO No.
        [Paragraph("DEPENDENCIA:", field_label_style), Paragraph(contratoOperativo.nombreSecretaria or "", field_value_style), Paragraph("CONTRATO No.", field_label_style), Paragraph(no_contrato, field_value_style)]
    ]
    form_table_dependencia_contrato = Table(form_data_dependencia_contrato, colWidths=[1.8*inch, 2.8*inch, 1.2*inch, 1.2*inch])
    form_table_style_dependencia_contrato = [
        # Padding en todos los lados (10 puntos cada uno)
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),

        # Borde de todos los lados
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

        
    ]
    form_table_dependencia_contrato.setStyle(form_table_style_dependencia_contrato)
    content.append(form_table_dependencia_contrato)
    content.append(Spacer(1, 20))

    # Sección de campos del formulario pt1
    # Crear campos del formulario
    form_data = [
        # NOMBRE
        [Paragraph("NOMBRE:", field_label_style), Paragraph(contratoOperativo.nombrePdS or "\u00A0", field_value_style)],
        
        # # SERVICIO REQUERIDO
        [Paragraph("SERVICIO REQUERIDO:", field_label_style), Paragraph(contratoOperativo.funcionesPsD or "\u00A0", field_value_style)],

        # # ÁREA EN LA QUE SE REQUIEREN LOS SERVICIOS
        [Paragraph("ÁREA EN LA QUE SE REQUIEREN LOS SERVICIOS:", field_label_style), Paragraph(contratoOperativo.puestoSolicitante or "\u00A0", field_value_style)],

        # DOMICILIO
        [Paragraph("DOMICILIO:", field_label_style), Paragraph(contratoOperativo.domicilioSecretaria or "\u00A0", field_value_style)],

        # # TITULAR DEL ÁREA
        [Paragraph("TITULAR DEL ÁREA:", field_label_style), Paragraph(contratoOperativo.nombreSolicitante or "\u00A0", field_value_style)],

        # # CARGO DEL TITULAR DE ÁREA
        [Paragraph("CARGO DEL TITULAR DE ÁREA:", field_label_style), Paragraph(contratoOperativo.puestoSolicitante or "\u00A0", field_value_style)],
        
        # # PERCEPCIÓN MENSUAL BRUTA
        # [Paragraph("PERCEPCIÓN MENSUAL BRUTA:", field_label_style), "", "", ""],
        # [Paragraph(f"${contratoOperativo.impMensualBruto:,.2f} ({contratoOperativo.montoLetra})" if contratoOperativo.impMensualBruto and contratoOperativo.montoLetra else "", field_value_style), 
        #  "", "", ""],
        
        # # AJUSTE DE SUELDO
        # [Paragraph("AJUSTE DE SUELDO:", field_label_style), "", "", ""],
        # [Paragraph(contratoOperativo.sueldoAnterior or "N/A", field_value_style), "", "", ""],
    ]
    
    # Crear tabla de campos
    form_table = Table(form_data, colWidths=[1.8*inch, 5.2*inch])
    
    form_table_style = [
        # Padding en todos los lados (10 puntos cada uno)
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Configuración del borde
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Línea superior
        # ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),  # Línea inferior
        #Líneas internas laterales
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),  # Línea izquierda
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),  # Línea derecha
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        
        # # Spans para campos que ocupan toda la fila (ahora para las variables de texto)
        ('SPAN', (0, 0), (0, 0)),   # NOMBRE |  valor
    ]
    
    form_table.setStyle(form_table_style)
    content.append(form_table)

    # Seccion de NUEVA CONTRATACIÓN y RENOVACIÓN
    # Obtener datos del contrato
    nuevo_checked = "X" if contratoOperativo.tipoContrato and "nuevo" in contratoOperativo.tipoContrato.lower() else "\u00A0\u00A0"
    renovacion_checked = "X" if contratoOperativo.tipoContrato and "renovación" in contratoOperativo.tipoContrato.lower() else "\u00A0\u00A0"
    form_data_renovacion_contratacion = [
        [Paragraph(f"NUEVA CONTRATACIÓN: <font name='Helvetica' size='12'>[{nuevo_checked}]</font>", field_label_style_center), Paragraph(f"RENOVACIÓN: <font name='Helvetica' size='12'>[{renovacion_checked}]</font>", field_label_style_center)]
    ]
    form_table_renovacion_contratacion = Table(form_data_renovacion_contratacion, colWidths=[3.5*inch, 3.5*inch])
    form_table_style_renovacion_contratacion = [
        # Padding en todos los lados (10 puntos cada uno)
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        # ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Configuración del borde (solo a los lados)
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black), # Línea izquierda
        ('LINEAFTER', (1, 0), (1, -1), 1, colors.black), # Línea derecha
        # Configuración de alineación vertical centrada y horizontal centrada
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]
    form_table_renovacion_contratacion.setStyle(form_table_style_renovacion_contratacion)
    content.append(form_table_renovacion_contratacion)

    # Seccion de FECHA INICIAL y FECHA DE TERMINACIÓN
    meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }
    anio_inicio = contratoOperativo.fechaInicioContrato.split("-")[0] if contratoOperativo.fechaInicioContrato else "\u00A0"
    mes_inicio = meses[int(contratoOperativo.fechaInicioContrato.split("-")[1])] if contratoOperativo.fechaInicioContrato else "\u00A0"
    dia_inicio = contratoOperativo.fechaInicioContrato.split("-")[2] if contratoOperativo.fechaInicioContrato else "\u00A0"
    anio_fin = contratoOperativo.fechaFinContrato.split("-")[0] if contratoOperativo.fechaFinContrato else "\u00A0"
    mes_fin = meses[int(contratoOperativo.fechaFinContrato.split("-")[1])] if contratoOperativo.fechaFinContrato else "\u00A0"
    dia_fin = contratoOperativo.fechaFinContrato.split("-")[2] if contratoOperativo.fechaFinContrato else "\u00A0"
    # Formatear fechas como "DD/MMMM/AAAA"
    fecha_formateada_inicio = dia_inicio + "/" + mes_inicio + "/" + anio_inicio if dia_inicio and mes_inicio and anio_inicio else "\u00A0"
    fecha_formateada_fin = dia_fin + "/" + mes_fin + "/" + anio_fin if dia_fin and mes_fin and anio_fin else "\u00A0"
    form_data_fi_ft = [
        # FECHA INICIAL y FECHA DE TERMINACIÓN
        [Paragraph("FECHA INICIAL:", field_label_style_center), Paragraph(fecha_formateada_inicio, field_value_style_center), Paragraph("FECHA DE TERMINACIÓN:", field_label_style_center), Paragraph(fecha_formateada_fin, field_value_style_center)]
    ]
    form_table_fi_ft = Table(form_data_fi_ft, colWidths=[1.75*inch, 1.75*inch, 1.75*inch, 1.75*inch])
    form_table_style_fi_ft = [
        # Padding solo en los lados (10 puntos cada uno)
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Configuración del borde (solo a los lados)
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black), # Línea izquierda
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black), # Línea derecha
        # Configuración de alineación vertical centrada y horizontal centrada
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]
    form_table_fi_ft.setStyle(form_table_style_fi_ft)
    content.append(form_table_fi_ft)

    # Sección de MONTO TOTAL DEL CONTRATO y Ajuste de sueldo
    monto_total_contrato = f"${contratoOperativo.impMensualBruto:,.2f} ({contratoOperativo.montoLetra})" if contratoOperativo.impMensualBruto and contratoOperativo.montoLetra else "\u00A0"
    monto_totalAnterior = f"${contratoOperativo.sueldoAnterior:,.2f} ({contratoOperativo.montoLetraAnterior})" if contratoOperativo.sueldoAnterior and contratoOperativo.montoLetraAnterior else "\u00A0"
    form_data_monto_total = [
        [Paragraph("MONTO TOTAL DEL CONTRATO:", field_label_style), Paragraph(monto_total_contrato, field_value_style_center)],
        [Paragraph("AJUSTE DE SUELDO:", field_label_style), Paragraph(monto_totalAnterior, field_value_style_center)]
    ]
    form_table_monto_total = Table(form_data_monto_total, colWidths=[1.8*inch, 5.2*inch])
    form_table_style_monto_total = [
        # Padding en todos los lados (10 puntos cada uno)
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        # ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Configuración del borde (solo a los lados)
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black), # Línea izquierda
        ('LINEAFTER', (1, 0), (1, -1), 1, colors.black), # Línea derecha
        # Configuración de alineación vertical centrada y horizontal centrada
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]
    form_table_monto_total.setStyle(form_table_style_monto_total)
    content.append(form_table_monto_total)

    # Espaciador antes de la sección de firmas
    # content.append(Spacer(1, 30))
    
    # Sección de FIRMAS
    signature_data = [
        ["SOLICITA", "", ""],
        ["", "", ""],  # Fila para la línea
        [f"{contratoOperativo.nombreSolicitante.title() if contratoOperativo.nombreSolicitante else 'NOMBRE DEL SOLICITANTE'}", "", ""],
        [f"{contratoOperativo.puestoSolicitante.title() if contratoOperativo.puestoSolicitante else 'PUESTO SOLICITANTE'}", "", ""],
        ["", "", ""]
    ]

    # Mantener el ancho total de 7*inch pero dividido en 3 columnas
    signature_table = Table(signature_data, colWidths=[1.5*inch, 4*inch, 1.5*inch], rowHeights=[1*inch, 0.1*inch, 0.3*inch, 0.1*inch, 0.3*inch])

    signature_table.setStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        # Línea solo en la columna central (índice 1) para la firma
        ('LINEBELOW', (1, 1), (1, 1), 1, colors.black),
        # Spans para que el contenido ocupe toda la fila visualmente
        ('SPAN', (0, 0), (2, 0)),  # SOLICITA ocupa las 3 columnas
        ('SPAN', (0, 2), (2, 2)),  # Nombre ocupa las 3 columnas
        ('SPAN', (0, 3), (2, 3)),  # Puesto ocupa las 3 columnas
        ('SPAN', (0, 4), (2, 4)),  # Última fila vacía ocupa las 3 columnas
    ])
    
    content.append(signature_table)
    
    # Construir el PDF
    doc.build(content)
    
    # Obtener el contenido del buffer y crear respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_tecnica_{contratoOperativo_id}.pdf"'
    response.write(pdf)
    
    return response

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_width, page_height = letter
    canvas.restoreState()    
    # Lista para almacenar el contenido del contrato

#####  AQUI TERMINA EL REPORTE DE CONTRADO DE LA SECRETARIA DE FINANZAS #####

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ContratoOperativo

def eliminar_archivo(request, contrato_id, pdf_key):
    try:
        contratoOperativo = get_object_or_404(ContratoOperativo, id=contrato_id)
        
        pdf_attr = pdf_key  # Usar el nombre de campo del PDF directamente
        
        pdf_field = getattr(contratoOperativo, pdf_attr)
        
        if pdf_field:
            pdf_field.delete()
            setattr(contratoOperativo, pdf_attr, None)
            contratoOperativo.save()
            return JsonResponse({'message': f'Archivo {pdf_key} eliminado correctamente'})
        else:
            return JsonResponse({'message': f'El contrato no tiene archivo {pdf_key} adjunto'})
    except ContratoOperativo.DoesNotExist:
        return JsonResponse({'message': 'Contrato no encontrado'}, status=404)


from django.shortcuts import render
from django.http import JsonResponse

def subir_archivo(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']

        # Validación: Asegúrate de que el archivo sea un PDF
        if not archivo.name.endswith('.pdf'):
            return JsonResponse({'error': 'El archivo no es un PDF válido.'}, status=400)
        
        try:
            # Ajusta la ruta al directorio donde deseas guardar los archivos
            with open('ruta/a/tu/directorio/' + archivo.name, 'wb') as destino:
                for chunk in archivo.chunks():
                    destino.write(chunk)
            return JsonResponse({'message': 'Archivo subido exitosamente.'})
        except Exception as e:
            return JsonResponse({'error': 'Error al subir el archivo: ' + str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido.'}, status=405)