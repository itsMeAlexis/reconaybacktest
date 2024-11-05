from django.urls import path
from . import views

app_name = 'contratos'

urlpatterns = [
    # Otras URL aquí si las tienes
    path('generar_pdf/<int:contrato_id>/', views.generate_PDF, name='generar_pdf'),
    path('generar_pdf_fin/<int:contrato_id>/', views.generate_PDF_FIN, name='generar_pdf_fin'),
    path('eliminar_archivo/<int:contrato_id>/<str:pdf_key>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('subir-archivo/', views.subir_archivo, name='subir_archivo'),
]