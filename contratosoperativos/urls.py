from django.urls import path
from . import views
from contratosoperativos.views import generate_PDF_Operativo
from contratosoperativos.views import generate_PDF_OperativoFIN

app_name = 'contratoOperativos'

urlpatterns = [
    # Otras URL aquí si las tienes
    path('generar_pdf_operativo/<int:contratoOperativo_id>/', views.generate_PDF_Operativo, name='generar_pdf_operativo'),
    path('generar_pdf_operativofin/<int:contratoOperativo_id>/', views.generate_PDF_OperativoFIN, name='generar_pdf_operativofin'),
    path('eliminar_archivo/<int:contrato_id>/<str:pdf_key>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('subir-archivo/', views.subir_archivo, name='subir_archivo'),   
]

