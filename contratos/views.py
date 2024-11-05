from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, PageTemplate, Frame, PageBreak, KeepInFrame
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from .models import Contrato
from contratos.models import Contrato
from reportlab.lib.units import mm
import locale
import datetime

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

#letter = (612, 792)  # Tamaño de la página letter (8.5 x 11 pulgadas)
def generate_PDF(request, contrato_id):

    contrato = get_object_or_404(Contrato, id=contrato_id)

    #no_contrato = contrato.noContrato 

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
        "justify": ParagraphStyle(name="Justify", fontName="Helvetica", fontSize=12, alignment=4),
        "right": ParagraphStyle(name="Right", fontName="Helvetica", fontSize=12, alignment=2),
        "space": lambda size: Spacer(1, size),  # Agregar función para el estilo "space"

    }
    # Establecer la configuración regional en español
    #locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

    # Define la fecha
    fecha_inicio_contrato = contrato.fechaInicioContrato
    fecha_fin_contrato = contrato.fechaFinContrato

    # Convierte la fecha en un objeto datetime
    fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio_contrato, "%Y-%m-%d")
    fecha_fin_obj = datetime.datetime.strptime(fecha_fin_contrato, "%Y-%m-%d")

    nombres_meses_espanol = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    # Obtén el nombre del mes
    nombre_mes_inicio = nombres_meses_espanol[fecha_inicio_obj.month-1]
    nombre_mes_fin = nombres_meses_espanol[fecha_fin_obj.month-1]
                    

    # Formatea la fecha en el formato deseado
    fecha_formateada_inicio = fecha_inicio_obj.strftime("%d de {} de %Y").format(nombre_mes_inicio)
    fecha_formateada_fin = fecha_fin_obj.strftime("%d de {} de %Y").format(nombre_mes_fin)

    # Estilo del párrafo
    #style = ParagraphStyle(
       # "custom",
       # alignment=TA_CENTER,
        #fontSize=12,
    #)
    
    #locale.setlocale(locale.LC_ALL, 'es-MX')

    no_contrato = contrato.noContrato if contrato.noContrato is not None else "&nbsp"
    #no_cedula = contrato.cedulaProf if contrato.cedulaProf is not None else "N/A"
    nombre_secretario_solicitante =  contrato.nombreSolicitante if contrato.nombreSecretaria == "SECRETARIA DE ADMINISTRACION Y FINANZA" or contrato.nombreSecretaria == "Secretaría de Administración y Finanzas" or contrato.nombreSecretaria == "SECRETARÍA DE ADMINISTRACIÓN Y FINANZA" or contrato.nombreSecretaria == "Secretaria de Administracion y Finanzas" or contrato.nombreSecretaria == "Secretaría de Administracion y Finanzas" or contrato.nombreSecretaria == "Secretaria de Administración y Finanzas" or contrato.nombreSecretaria == "SECRETARÍA DE ADMINISTRACION Y FINANZA" or contrato.nombreSecretaria == "SECRETARIA DE ADMINISTRACIÓN Y FINANZA"  else contrato.nombreSecretario

    puesto_secretario_solicitante =  contrato.puestoSolicitante if contrato.nombreSecretaria == "SECRETARIA DE ADMINISTRACION Y FINANZAS" or contrato.nombreSecretaria == "Secretaría de Administración y Finanzas" else contrato.puestoSecretario
    #Usando operador ternario para tituloProf
    #titulo_profesional = contrato.tituloProf.upper() if contrato.tituloProf else "Título no especificado"

    # Usando operador ternario para cedulaProf
    cedula_profesional = contrato.cedulaProf.upper() if contrato.cedulaProf else "N/A"

        
    paragraphs =[   
        
        "<para align='right'><b>CONTRATO No:</b><b><u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u></b></para>".format(no_contrato),

        "<para>&nbsp;</para>",
        
        "<para align='right'><b>IMPORTE MENSUAL BRUTO $:</b><b><u>&nbsp;&nbsp;&nbsp;&nbsp;" + f"{contrato.impMensualBruto:,.2f}" + "&nbsp;&nbsp;&nbsp;&nbsp;</u></b></para>",
        
        "<para>&nbsp;</para>",
        
        "<para align='justify'><b>CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES SUJETO AL PAGO DE HONORARIOS BAJO EL RÉGIMEN FISCAL DE INGRESOS ASIMILADOS A SALARIOS, POR TIEMPO DETERMINADO,</b> QUE CELEBRAN POR UNA PARTE, EL PODER EJECUTIVO DEL ESTADO DE NAYARIT A TRAVÉS DE LA SECRETARÍA DE ADMINISTRACIÓN Y FINANZAS, REPRESENTADA EN ESTE ACTO POR EL <b>DIRECTOR GENERAL DE ADMINISTRACIÓN, LIC JUAN ALBERTO PINEDA CISNEROS</b>, A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ “<b>LA DEPENDENCIA</b>” Y POR LA OTRA PARTE, EL(A) C. <u>&nbsp;&nbsp; " +  contrato.nombrePdS.upper() + " &nbsp;&nbsp;</u> EN LO SUCESIVO “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, A QUIENES AL ACTUAR EN CONJUNTO SE LES DENOMINARÁ “<b>LAS PARTES</b>” AL TENOR DE LOS ANTECEDENTES, DECLARACIONES Y CLÁUSULAS SIGUIENTES:</para>",

        "<para>&nbsp;</para>",

        "<para align='center'><b>ANTECEDENTES</b></para>",

        "<para>&nbsp;</para>",
        
        "<para align='justify'>Que en fecha <u>&nbsp;&nbsp; " + contrato.fechaOficio.upper() + "&nbsp;&nbsp;</u>, mediante Oficio No. <u>&nbsp;&nbsp;" + contrato.NoOficio.upper() + "&nbsp;&nbsp;</u>, firmado por el(a) <u>&nbsp;&nbsp;" + nombre_secretario_solicitante +"&nbsp;&nbsp;</u>, en su carácter de <u>&nbsp;&nbsp;" + puesto_secretario_solicitante + "&nbsp;&nbsp;</u>, solicitó al SECRETARIO DE ADMINISTRACION Y FINANZAS DEL PODER EJECUTIVO DEL ESTADO DE NAYARIT, <b>MTRO. EN FISCAL JULIO CESAR LÓPEZ RUELAS</b>, que con cargo al Presupuesto del(a) <u>&nbsp;&nbsp; " + contrato.nombreSecretaria.upper() + "&nbsp;&nbsp;</u>, celebrara Contrato Civil de Prestación de Servicios Profesionales sujeto al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por tiempo determinado, con el(a) C.<u>&nbsp;&nbsp;" + contrato.nombrePdS.upper() + "&nbsp;&nbsp;</u>, para que a partir del día&nbsp; " + fecha_formateada_inicio + ", preste los servicios profesionales que se describen en la Cláusula PRIMERA de este instrumento, el cual se encuentra debidamente autorizado por el Titular del Poder Ejecutivo, en términos del documento que se adjunta.</para>".format(nombre_secretario_solicitante),

        "<para>&nbsp;</para>",

        "<para align='center'><b>DECLARACIONES</b></para>",

        "<para>&nbsp;</para>",

        "<para><b>1.- DECLARA “LA DEPENDENCIA”, A TRAVÉS DE SU REPRESENTANTE, QUE:</b></para>",

        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.1.-</b>La Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, forma parte de la Administración Pública Centralizada del Gobierno del Estado de Nayarit, de conformidad con lo establecido en el artículo 72 de la Constitución Política del Estado Libre y Soberano de Nayarit, y los artículos 1 y 31 fracción II de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit; y tiene entre sus atribuciones el coordinar la planeación y aplicación de la política administrativa, financiera, crediticia, fiscal, hacendaria y del gasto público de la Administración Pública Estatal, además de normar y regular la prestación de servicios administrativos que requieran las Dependencias; lo anterior, con fundamento en lo dispuesto en el artículo 33 de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit.</para> ", 

        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.2.-</b>Su representante, el Director General de Administración de la Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, participa en la celebración del presente instrumento con fundamento en los artículos 19 y 26 de la Ley Orgánica del Poder Ejecutivo del Estado de Nayarit, y los artículos 9, fracción VII, y 67 fracción XIV, del Reglamento Interior de la Secretaría de Administración y Finanzas, y demás normativa aplicable; quien acredita su personalidad con el nombramiento expedido a su favor por el Titular de la Secretaría de Administración y Finanzas del Poder Ejecutivo del Estado de Nayarit, Mtro. en Fiscal Julio César López Ruelas, de fecha 16 de febrero de 2023.</para>",

        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.3.-</b> Su representada está inscrita en el Registro Federal de Contribuyentes con la clave SAD091223KK7, con domicilio fiscal sito en Avenida México sin número, Centro, Tepic Nayarit, C.P. 63000, mismo que señala para todos los efectos que se derivan del presente contrato.</para>",

        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.4.-</b> De acuerdo a las necesidades propias del(a) <u>&nbsp;&nbsp;" + contrato.nombreSecretaria.upper() + "&nbsp;&nbsp;</u>, se requiere temporalmente la contratación de los servicios profesionales de “<b>EL(A) PRESTADOR(A) DE SERVICIOS)</b>”, sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, para llevar a cabo las acciones materia de este contrato, consistentes en <u>&nbsp;&nbsp;" + contrato.funcionesProf.upper() + "&nbsp;&nbsp;</u>.</para>",

        "<para>&nbsp;</para>",

        "<para align='justify'><b>1.5.-</b> Cuenta con la disponibilidad presupuestal para el pago de los servicios requeridos, motivo del presente contrato, afectando la partida presupuestal número 12101 del Presupuesto de Egresos del Estado Libre y Soberano de Nayarit para el Ejercicio Fiscal 2024.</para>",
        
        "<para>&nbsp;</para>",

        "<b>2.- DECLARA “EL(A) PRESTADOR(A) DE SERVICIOS” , QUE: </b>,",

        "<para>&nbsp;</para>",
        
        "<para align='justify'><b>2.1.-</b> Tiene la capacidad jurídica para contratar y obligarse en los términos del presente instrumento civil, y que cuenta con los conocimientos profesionales y la experiencia necesaria para prestar los servicios profesionales que requiere “<b>LA DEPENDENCIA</b>”.</para>",
   
        "<para>&nbsp;</para>",

        "<para align='justify'><b>2.2.-</b> Ostenta título de <u>&nbsp;&nbsp;{0}&nbsp;&nbsp;</u>, expedido por <u>&nbsp;&nbsp;{1}&nbsp;&nbsp;</u>. Con número de Cédula Profesional <u>&nbsp;&nbsp;{2}&nbsp;&nbsp;</u>, expedida por la Dirección General de Profesiones de la Secretaría de Educación Pública.</para>".format(contrato.tituloProf.upper(), contrato.institucionExpTituloProf.upper(), cedula_profesional),

        "<para>&nbsp;</para>",  
       
        "<para align='justify'><b>2.3.-</b> Es una persona física de nacionalidad mexicana, de <u>&nbsp;&nbsp;" +contrato.edadPdS.upper() + " &nbsp;&nbsp;</u> años, sexo <u>&nbsp;&nbsp;" + contrato.sexoPdS.upper() + "&nbsp;&nbsp;</u>, estado civil <u>&nbsp;&nbsp;" + contrato.estadoCivilPdS.upper() + "&nbsp;&nbsp;</u>, C.U.R.P. <u>&nbsp;&nbsp;" + contrato.curpdS.upper() +"&nbsp;&nbsp;</u>, correo electrónico <u>&nbsp;&nbsp;" + contrato.emailPdS.upper() + "&nbsp;&nbsp;</u>; credencial para votar vigente, con clave <u>&nbsp;&nbsp;" + contrato.inePdS.upper() + "&nbsp;&nbsp;</u> y que su domicilio particular para los efectos legales de este contrato es el ubicado en <u>&nbsp;&nbsp;" + contrato.domicilioPdS.upper() + "&nbsp;&nbsp;</u>C.P.<u>&nbsp;&nbsp; " + contrato.cpPdS.upper() +"&nbsp;&nbsp;</u>.</para>",

        "<para>&nbsp;</para>",       
    
        "<para align='justify'><b>2.4.-</b> Está inscrita(o) en el Registro Federal de Contribuyentes, bajo el número <u>&nbsp;&nbsp;" + contrato.rfcPdS.upper() + "&nbsp;&nbsp;</u>, y está al corriente del cumplimiento de sus obligaciones fiscales, tal y como lo acredita con constancia de situación fiscal actualizada.</para> ",

        "<para>&nbsp;</para>",  
        
        "<para align='justify'><b>2.5.-</b> Ha sido su voluntad ofrecer a “<b>LA DEPENDENCIA</b>” los servicios objeto del presente contrato, bajo el régimen fiscal de honorarios asimilados a salarios y por tiempo determinado, empleando todos sus conocimientos, capacidades técnicas y tiempo que sea necesario para el cabal cumplimiento del presente contrato.</para> ",
        
        "<para>&nbsp;</para>",

        "<para align='justify'><b>2.6.-</b>Es una persona física ajena a “<b>LA DEPENDENCIA</b>” por lo que puede denominársele el(la) “<b>PRESTADOR(A) DE SERVICIOS</b>”, que presta sus servicios de manera independiente a toda persona física o moral que le solicite la prestación de sus servicios y que su actividad profesional no la presta preponderantemente a “<b>LA DEPENDENCIA</b>”.</para>",

        "<para>&nbsp;</para>",
        
        "<para align='justify'><b>2.7.-</b>La prestación de los servicios profesionales a que se refiere este contrato es de naturaleza civil, sujeta al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por tiempo determinado, que se encuentra regulada por el Título IV, Capítulo II, de la Ley del Impuesto sobre la Renta vigente.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>2.8.-</b> Se obliga a someterse a los términos del presente contrato de prestación de servicios profesionales de naturaleza civil, en virtud de que este instrumento no se considera en ningún momento contrato laboral. Por ello “<b>LA DEPENDENCIA</b>”, no será patrón directo ni indirecto, y no contrae obligación, ni responsabilidad alguna al respecto.</para>",

        "<para>&nbsp;</para>",
    
        "<para align='justify'><b>2.9.-</b> Manifiesta su conformidad para que “<b>LA DEPENDENCIA</b>” realice los descuentos a los honorarios que por el presente contrato se generen y se realicen los pagos correspondientes ante las autoridades hacendarias, conforme a lo dispuesto en el artículo 94 fracción IV de la Ley del Impuesto sobre la Renta, para los efectos fiscales a que haya lugar.</para>",

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
        
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”por virtud del presente instrumento, se obliga civilmente a prestar a “<b>LA DEPENDENCIA</b>”, sus servicios profesionales, con el objeto de <u>&nbsp;&nbsp;" + contrato.funcionesProf.upper() + "&nbsp;&nbsp;</u></para>",

        "<para>&nbsp;</para>",

        "<b>SEGUNDA.-</b>CONDICIONES GENERALES.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” se obliga a prestar los servicios señalados en la Cláusula inmediata anterior, con toda diligencia, obligándose a aportar toda su experiencia y capacidad, dedicando todo el tiempo que considere necesario para dar cabal cumplimiento al presente contrato, ello sin estar sujeta a un horario, dada la especial naturaleza del presente contrato, pudiendo “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” realizar sus tareas en los tiempos y formas que estime pertinentes. Estando “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, no obstante la vigencia del presente contrato, en plena libertad de ofertar sus servicios profesionales a otros entes públicos o privados.</para> ",

        "<para>&nbsp;</para>",
       
        "<para align='justify'>Toda la información que obtenga “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” de “<b>LA DEPENDENCIA</b>”, y viceversa, será manejada en forma confidencial y sólo podrá ser usada para cumplir con los fines del presente contrato.</para>",

        "<para>&nbsp;</para>",
        
        "<b>TERCERA.-</b>IMPORTE DEL CONTRATO.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>LA DEPENDENCIA</b>” se obliga a cubrir por concepto de honorarios a “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” por la prestación de Servicios Profesionales sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, a que se refiere este contrato, la cantidad de <u>&nbsp;&nbsp;&nbsp;" +  f"{contrato.impMensualBruto,'%.2f'}" + "&nbsp;&nbsp;&nbsp;</u> cantidad con letra <u>&nbsp;&nbsp;" + contrato.montoLetra.upper() + "&nbsp;&nbsp;</u>  mensuales, que podrá ser distribuida en percepciones quincenales, efectuando la retención del Impuesto Sobre la Renta correspondiente en términos de los artículos 94 fracción IV y 96 de la Ley del Impuesto Sobre la Renta y demás correlativos aplicables.</para>",

        "<para>&nbsp;</para>",

        "<para align='justify'>Los pagos se harán “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” mediante dispersión electrónica en una cuenta bancaria personal, tramitada para tal efecto por la Dirección de Pago Electrónico de Servicios Personales de la Dirección General de Tesorería de la Secretaría de Administración y Finanzas.</para> ",

        "<para>&nbsp;</para>",
        
        "<para align='justify'>Queda bajo la responsabilidad de la Unidad Administrativa solicitante informar a la Secretaría de Administración y Finanzas de cualquier movimiento que se realice con motivo del presente contrato, así como del cumplimiento o incumplimiento por parte de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”.</para> ",

        "<para>&nbsp;</para>",
        
        "<b>CUARTA.-</b> VIGENCIA DEL CONTRATO.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>El presente contrato civil tendrá una vigencia improrrogable  del día &nbsp; " + fecha_formateada_inicio + " &nbsp;y hasta el &nbsp; " + fecha_formateada_fin + " . Concluida la vigencia no podrá haber prórroga automática por el simple transcurso del tiempo y terminará sin necesidad de darse aviso entre “<b>LAS PARTES</b>”. Para el caso de que “<b>LA DEPENDENCIA</b>” tuviera necesidad de contar nuevamente con los servicios de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, se requerirá la celebración de un nuevo contrato.</para>",

        "<para>&nbsp;</para>",

        "<b>QUINTA.-</b> VIGILANCIA.",

        "<para>&nbsp;</para>",
   
        "<para align='justify'>“<b>LA DEPENDENCIA</b>” a través de los representantes que para tal efecto designe, tendrá en todo tiempo el derecho de vigilar el estricto cumplimiento de este contrato civil, por lo que podrá revisar e inspeccionar las actividades desempeñadas por “<b>LA PRESTADORA DE SERVICIOS</b>”.</para>",
        
        "<para>&nbsp;</para>",
       
        "<b>SEXTA.-</b> NATURALEZA DE LA RELACIÓN.",

        "<para>&nbsp;</para>",
   
        "<para align='justify'>“<b>LAS PARTES</b>” quedan liberadas de otorgarse prestaciones propias de una relación de trabajo, por estar frente a un contrato de prestación de servicios profesionales de naturaleza civil.</para>",

        "<para>&nbsp;</para>",
        
        "<b>SÉPTIMA.-</b> INFORMES DE LOS SERVICIOS.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” mantendrá informada verbalmente o por escrito en el caso de así habérselo solicitado a la requirente de servicio, por conducto del titular del área solicitante, del estado que guardan las actividades materia del presente contrato.</para>",

        "<para>&nbsp;</para>",
     
        "<b>OCTAVA.-</b> IMPEDIMENTO.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” no podrá, en ningún momento y por ninguna razón, ceder o subrogar los derechos y obligaciones derivados del presente instrumento a terceras personas físicas y/o morales.</para> ",
        
        "<para>&nbsp;</para>",

        "<b>NOVENA.-</b> MODIFICACIONES.",

        "<para>&nbsp;</para>",

        "<para align='justify'>Cualquier variación en lo pactado en este contrato de prestación de servicios profesionales, será acordada por “<b>LAS PARTES</b>” en forma previa y escrita, celebrando para ello el convenio modificatorio correspondiente, debiendo,para su validez, estar firmado por ambas partes, señalarse claramente que se trata de una modificación, y se determine su alcance. En el entendido de que cualquier convenio verbal es y será nulo.</para> ",

        "<para>&nbsp;</para>",
        
        "<b>DÉCIMA.- “EL(A) PRESTADOR(A) DE SERVICIOS</b>”, SE COMPROMETE A LO SIGUIENTE: ",

        "<para>&nbsp;</para>",
        
        "<para align='justify'>a) No divulgar ni dar a conocer los datos y documentos que “<b>LA DEPENDENCIA</b>” le proporcione para las actividades que desarrolla, ni dar informes a personas distintas a las señaladas por ella.</para>",

        "<para>&nbsp;</para>",
     
        "<para align='justify'>b) Ser directamente responsable de los daños y perjuicios que cause a “<b>LA DEPENDENCIA</b>” y/o a terceros, por negligencia, impericia, omisión o dolo en la prestación de los servicios que se obliga a realizar. </para>",

        "<para>&nbsp;</para>",

        "<b>DÉCIMA PRIMERA.-</b>INFORMACIÓN GENERADA.",

        "<para>&nbsp;</para>",
    
        "<para align='justify'>“<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” manifiesta que todos los bienes, técnicas, licencias, manuales de operación, guías, material bibliográfico, y demás materiales y equipos que utilice para la prestación del servicio objeto de éste contrato, distintos a aquellos que le sean proporcionados por “<b>LA DEPENDENCIA</b>” y sean propiedad de “<b>LA DEPENDENCIA</b>”, son de su propiedad, o no siéndolos, cuenta con los permisos, autorizaciones y licencias correspondientes para su uso y utilización, liberando a la “<b>LA DEPENDENCIA</b>” de cualquier responsabilidad derivada del uso y utilización de los mismos.</para>",

        "<para>&nbsp;</para>",
         
        "<para align='justify'>Aunado a lo anterior, “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” manifiesta estar enterado de que todos los archivos, documentación y/o información que genere al prestar sus servicios profesionales independientes a “<b>LA DEPENDENCIA</b>” será propiedad de la segunda, y por ningún motivo podrá disponer de ella para asuntos y/o situaciones distintas a la prestación de sus servicios, y en todo caso, una vez finalizada la contraprestación de los mismos, no podrá utilizar ni reproducir archivos, documentación y/o información alguna; así mismo, al tratarse de propiedad de “<b>LA DEPENDENCIA</b>”, “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” no podrá eliminar física ni digitalmente tales archivos, documentación y/o información.</para>",

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
    
        "<para align='justify'>Para la interpretación y cumplimiento del presente contrato, “<b>LAS PARTES</b>” se someten a la jurisdicción y competencia de los Juzgados Civiles de la ciudad de Tepic, Nayarit, así como a las disposiciones contenidas en el Código Civil para el Estado de Nayarit vigente, renunciando expresamente al fuero que pudiera corresponderles en razón de su domicilio actual o futuro.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>DÉCIMA QUINTA</b>.- Queda expresamente convenido que la falta de cumplimiento a cualquiera de las obligaciones que aquí se contraen y aquellas otras que dimanan del Código Civil para el Estado de Nayarit vigente, será motivo de rescisión del presente contrato y derivará además en el pago de los daños y perjuicios que el incumplimiento cause a la parte que cumple.</para>",

        "<para>&nbsp;</para>",
   
        "<para align='justify'><b>DÉCIMA SEXTA</b>.- “<b>LAS PARTES</b>” quedan obligadas a dar cumplimiento a las cláusulas del presente instrumento jurídico sujetándose a lo dispuesto por el Código Civil para el Estado de Nayarit, por tratarse de un contrato de prestación de servicios profesionales sujetos al pago de honorarios bajo el régimen fiscal de Ingresos Asimilados a Salarios, por consiguiente, quedan liberadas de otorgarse prestaciones propias de una relación de trabajo, por lo que “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>” releva a “<b>LA DEPENDENCIA</b>” de cualquier responsabilidad presente o futura por este concepto.</para>",

        "<para>&nbsp;</para>",
       
        "<para align='justify'><b>DÉCIMA SÉPTIMA</b>.- En razón del correcto y cabal cumplimiento del presente contrato por parte de “<b>EL(A) PRESTADOR(A) DE SERVICIOS</b>”, “<b>LA DEPENDENCIA</b>” tendrá total independencia para considerar entregarle un bono de gratificación, que podría otorgarse por un monto equivalente de hasta dos meses, respecto a lo señalado en la Cláusula TERCERA, indistintamente del período del término del contrato, siempre y cuando se cuente con la disponibilidad presupuestal en el ejercicio fiscal de que se trate, y a discrecionalidad de “<b>LA DEPENDENCIA</b>”, por tal motivo, no constituye una obligación para “<b>LA DEPENDENCIA</b>”.</para>",

         "<para>&nbsp;</para>",
            
        "<para align='justify'>Leído que fue el presente contrato y enteradas las partes del contenido y alcance de todas y cada una de sus cláusulas, lo firman por duplicado, ante los testigos que al final suscriben, en la Ciudad de Tepic, Nayarit, el día&nbsp; " + fecha_formateada_inicio + ".</para>",
         
         
        
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
    
    content = []
    # Lista para almacenar los párrafos formateados
   
    
    # Aplicar estilos a cada párrafo y agregarlos a la lista
    for para in paragraphs:
        elements = apply_style(para, styles_to_apply)
        
       


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
            Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.nombrePdS.upper()}&nbsp;&nbsp;" + " </b>", centered_style)],
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style),],         
            [Paragraph("<b>ÁREA SOLICITANTE</b>", centered_style),
            Paragraph(""),
            Paragraph("<b>TESTIGO</b>", centered_style)],         
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style)],
            [Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.nombreSolicitante.upper()}&nbsp;&nbsp;" + " </b>", centered_style),
            Paragraph(""),
            Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.nombreTestigo.upper()}&nbsp;&nbsp;" + "</b>", centered_style)],               
            [Paragraph(f"&nbsp;&nbsp;{contrato.puestoSolicitante.upper()}&nbsp;&nbsp;", centered_style_2),
            Paragraph(""),
            Paragraph(f"&nbsp;&nbsp;{contrato.puestoTestigo.upper()}&nbsp;&nbsp;", centered_style_2),
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


   
    # Envolver la tabla en KeepTogether
    table_keep_together = KeepTogether([table])
    #content.append(table_keep_together)
    
    buffer = BytesIO()
    top_margin = 60  # Ajustar según tus preferencias
    bottom_margin = 60  # Ajustar según tus preferencias
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=top_margin, bottomMargin=bottom_margin)

    # Definir un marco que cubra toda la página
    page_width, page_height = letter
    frame = Frame(0, 0, page_width, page_height, id='normal', leftPadding=72, rightPadding=72,
                  topPadding=top_margin, bottomPadding=bottom_margin)

    # Crear el PageTemplate con el marco definido
    page_template = PageTemplate(id='main', frames=[frame], onPage=header_footer)

    # Agregar el PageTemplate al SimpleDocTemplate
    doc.addPageTemplates([page_template])

    
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

    content.append(Spacer(1, 12))
    content.append(table_keep_together)
    page_template = PageTemplate(id='main', frames=[frame], onPage=header_footer)  #agregue
    
    doc.build(content, canvasmaker=PageNumCanvas)
   
    

    # Obtener el contenido del buffer y crear una respuesta HTTP con el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato_id}.pdf"'
    response.write(pdf)
    
    

    return response

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_width, page_height = letter    
    canvas.restoreState()    
   
#### INICIO DEL REPORTE DE SECRETARIA DE FINANZAS ####

def generate_PDF_FIN(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

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
    fecha_inicio_contrato = contrato.fechaInicioContrato
    fecha_fin_contrato = contrato.fechaFinContrato

    # Convierte la fecha en un objeto datetime
    fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio_contrato, "%Y-%m-%d")
    fecha_fin_obj = datetime.datetime.strptime(fecha_fin_contrato, "%Y-%m-%d")

    nombres_meses_espanol = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    # Obtén el nombre del mes
    
    nombre_mes_inicio = nombres_meses_espanol[fecha_inicio_obj.month-1]
    nombre_mes_fin = nombres_meses_espanol[fecha_fin_obj.month-1]
                    
             
    # Formatea la fecha en el formato deseado
    fecha_formateada_inicio = fecha_inicio_obj.strftime("%d de {} de %Y").format(nombre_mes_inicio)
    fecha_formateada_fin = fecha_fin_obj.strftime("%d de {} de %Y").format(nombre_mes_fin)

    no_contrato = contrato.noContrato if contrato.noContrato is not None else "&nbsp"    

    

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
    left_aligned_style = ParagraphStyle(
        'Center',
        fontSize=9,
        parent=styles['Normal'],
        alignment=TA_CENTER,
        
    )
    left_aligned_style = ParagraphStyle('LeftAligned', parent=styles['Normal'], alignment=TA_LEFT)

    
    
    
    data = [
            

            [Paragraph("<b>FICHA TÉCNICA DE VALIDACIÓN</b>",centered_style)],

            [Paragraph("CONTRATOS DE PRESTACIÓN DE SERVICIOS PROFESIONALES SUJETOS AL PAGO DE HONORARIOS",centered_style )],
            
            [Paragraph("BAJO EL RÉGIMEN FISCAL DE INGRESOS ASIMILADOS A SALARIOS",centered_style )],                      

            [Paragraph("<b>DEPENDENCIA:</b>", left_aligned_style),            
            Paragraph( f"&nbsp;&nbsp;{contrato.nombreSecretaria.upper()}&nbsp;&nbsp;" , left_aligned_style)],

             [Paragraph("<b>NOMBRE PRESTADOR DE SERVICIO:</b>", left_aligned_style),           
            Paragraph(f"&nbsp;&nbsp;{contrato.nombrePdS.upper()}&nbsp;&nbsp;", left_aligned_style),],         

            [Paragraph("<b>TELÉFONO:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.telefonoPdS.upper()}&nbsp;&nbsp;", left_aligned_style),
            Paragraph("<b>NO DE CONTRATO:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.noContrato}&nbsp;&nbsp;", left_aligned_style),],

            [Paragraph("<b>SERVICIO REQUERIDO:</b>", left_aligned_style),           
            Paragraph(f"&nbsp;&nbsp;{contrato.funcionesProf.upper()}&nbsp;&nbsp;", left_aligned_style),],   

            [Paragraph("<b>ÁREA EN LA QUE SE REQUIEREN LOS SERVICIOS:</b>", left_aligned_style),           
            Paragraph(f"&nbsp;&nbsp;{contrato.puestoSolicitante.upper()}&nbsp;&nbsp;", left_aligned_style)],         

            [Paragraph("<b>DOMICILIO DE LA DEPENDENCIA:</b>", left_aligned_style),           
            Paragraph(f"&nbsp;&nbsp;{contrato.domicilioSecretaria.upper()}&nbsp;&nbsp;", left_aligned_style)],

            [Paragraph("<b>TITULAR DEL ÁREA:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.nombreSolicitante.upper()}&nbsp;&nbsp;", left_aligned_style)],     

            [Paragraph("<b>CARGO DEL TITULAR DE ÁREA:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.puestoSolicitante.upper()}&nbsp;&nbsp;", left_aligned_style)],
           
            [Paragraph("<b>TIPO CONTRATO NUEVO/RENOVACIÓN:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.tipoContrato.upper()}&nbsp;&nbsp;", left_aligned_style)],

            [Paragraph("<b>FECHA INICIAL:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.fechaInicioContrato}&nbsp;&nbsp;", left_aligned_style),
            Paragraph("<b>FECHA DE TERMINACIÓN:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.fechaFinContrato}&nbsp;&nbsp;", left_aligned_style)
            ],           

            [Paragraph("<b>PERCEPCIÓN MENSUAL NETA:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.impMensualBruto}&nbsp;&nbsp;", left_aligned_style),
            Paragraph("<b>PERCEPCIÓN MENSUAL NETA CON LETRA:</b>", left_aligned_style),            
            Paragraph(f"{contrato.montoLetra}&nbsp;&nbsp;", left_aligned_style),
            ],

            [Paragraph("<b>AJUSTE DE SUELDO:</b>", left_aligned_style),            
            Paragraph(f"&nbsp;&nbsp;{contrato.sueldoAnterior}&nbsp;&nbsp;", left_aligned_style),
            Paragraph("<b>AJUSTE DE SUELDO CON LETRA:</b>", left_aligned_style),            
            Paragraph(f"{contrato.montoLetraAnterior.upper()}&nbsp;&nbsp;", left_aligned_style),],            

            [Paragraph("<b>ÁREA SOLICITANTE</b>", centered_style),
             Paragraph("<br/><br/><br/>", centered_style),
             Paragraph("<b>ÁREA QUE APRUEBA</b>", centered_style)        
            ],
            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style)],

            [Paragraph(f"&nbsp;&nbsp;{contrato.nombreSolicitante.upper()}&nbsp;&nbsp;", centered_style),
             Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(f"&nbsp;&nbsp;{contrato.nombreSecretario.upper()}&nbsp;&nbsp;", centered_style)],

            [Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.puestoSolicitante.upper()}&nbsp;&nbsp;" + " </b>", centered_style),
            Paragraph("<br/><br/><br/>", centered_style),
            Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.puestoSecretario.upper()}&nbsp;&nbsp;" + " </b>", centered_style)
            ],

            [Paragraph("<br/>", centered_style)],

            [Paragraph("<b>ÁREA Vo.Bo.</b>", centered_style)],

            [Paragraph("<br/><br/><br/>", centered_style),
            Paragraph(""),
            Paragraph("<br/><br/><br/>", centered_style)],

            [Paragraph(f"&nbsp;&nbsp;{contrato.nombreVobo.upper()}&nbsp;&nbsp;", centered_style)], 

            [Paragraph("<b>" + f"&nbsp;&nbsp;{contrato.puestoVobo.upper()}&nbsp;&nbsp;" + " </b>", centered_style)],   
            
        ]
      

    table = Table(data, colWidths=[150,116,133,133], style=[
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agregar bordes a todas las celdas
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear el contenido al centro de las celdas horizontalmente
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinear el contenido al centro de las celdas verticalmente
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Especificar la fuente en negrita (Helvetica-Bold)
        #('LINEBELOW', (0, 0), (0, 0), 1, colors.black),  # Subrayar solo la primera fila
        ('LINEBELOW', (0, 0), (3, 1), 1, colors.white),  # Subrayar solo la primera celda de la segunda fila (parte inferior)
        ('LINEBELOW', (0, 15), (0, 1), 1, colors.white),  # Subrayar solo la 
        ('LINEBELOW', (0, 1), (0, 1), 1, colors.white),  # Subrayar solo la primera celda de la segunda fila (parte inferior)
        ('LINEBELOW', (1, 1), (1, 1), 1, colors.white),  # Subrayar solo la segunda celda de la segunda fila (parte inferior)
        ('LINEBELOW', (0, 5), (0, 5), 1, colors.black),  # Subrayar solo la primera celda de la cuarta fila (parte inferior)
        ('LINEBELOW', (2, 5), (2, 5), 1, colors.black),  # Subrayar solo la segunda celda de la cuarta fila (parte inferior) 
         
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (1, 3), (3, 3)),
        ('SPAN', (1, 4), (3, 4)),
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (-1, 1)),        
        ('SPAN', (0, 2), (-1, 2)),
        ('SPAN', (1, 5), (1, 5)), 
        ('SPAN', (1, 6), (3, 6)),        
        ('SPAN', (1, 7), (3, 7)),    
        ('SPAN', (1, 8), (3, 8)),
        ('SPAN', (1, 9), (3, 9)),
        ('SPAN', (1, 10), (3, 10)),
        ('SPAN', (1, 11), (3, 11)),
        ('SPAN', (0, 15), (1, 15)),
        ('SPAN', (2, 15), (3, 15)),
        ('SPAN', (0, 16), (1, 16)),
        ('SPAN', (2, 16), (3, 16)),
        ('SPAN', (0, 17), (1, 17)),
        ('SPAN', (2, 17), (3, 17)),
        ('SPAN', (0, 18), (1, 18)),
        ('SPAN', (2, 18), (3, 18)),
        ('SPAN', (0, 19), (3, 19)),
        ('SPAN', (0, 20), (3, 20)),
        ('SPAN', (0, 21), (3, 21)),
        ('SPAN', (0, 22), (3, 22)),
        ('SPAN', (0, 23), (3, 23)),     
    ])
    
    

    buffer = BytesIO()
    top_margin = 70  # Ajustar según tus preferencias
    bottom_margin = 70  # Ajustar según tus preferencias
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=top_margin, bottomMargin=bottom_margin)

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

   
    content.append(table)
    #content.append(table2)
    page_template = PageTemplate(id='main', frames=[frame], onPage=header_footer)  #agregue
    #content = [formatted_paragraphs]  # Agregar formatted_parrafo a la lista content
    doc.build(content, canvasmaker=PageNumCanvas)
    #doc.build(canvasmaker=PageNumCanvas)
        
    # Obtener el contenido del buffer y crear una respuesta HTTP con el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato_id}.pdf"'
    response.write(pdf)

    return response

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_width, page_height = letter
    canvas.restoreState()    
    # Lista para almacenar el contenido del contrato

#####  AQUI TERMINA EL REPORTE DE CONTRADO DE LA SECRETARIA DE FINANZAS #####

#Eliminara archivo pdf
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Contrato

def eliminar_archivo(request, contrato_id, pdf_key):
    try:
        contrato = get_object_or_404(Contrato, id=contrato_id)
        
        pdf_attr = pdf_key  # Usar el nombre de campo del PDF directamente
        
        pdf_field = getattr(contrato, pdf_attr)
        
        if pdf_field:
            pdf_field.delete()
            setattr(contrato, pdf_attr, None)
            contrato.save()
            return JsonResponse({'message': f'Archivo {pdf_key} eliminado correctamente'})
        else:
            return JsonResponse({'message': f'El contrato no tiene archivo {pdf_key} adjunto'})
    except Contrato.DoesNotExist:
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