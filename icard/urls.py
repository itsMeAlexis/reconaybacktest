"""
URL configuration for icard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

 # include todavia no se necesita
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions

#from contratos.views import generatePDF

from django.views.static import serve #pdf


from users.api.router import router_user
from dependencias.api.router import router_dependencia
from contratos.api.router import router_contrato
from fichastecnicas.api.router import router_fichatecnica
from contratosoperativos.api.router import router_contratooperativo
#from .views import generatePDF

#from django.urls import path

from contratos.views import generate_PDF
from contratosoperativos.views import generate_PDF_Operativo
from contratosoperativos.views import generate_PDF_OperativoFIN
from django.urls import path
#from .contratos import views

#from contratos.views import generatePDF



schema_view = get_schema_view(
    openapi.Info(
        title="Contratos - ApiDoc",
        default_version='v1',
        description="Documentacion de la API Contratos",
        terms_of_service="https://www.hacienda-nayarit.gob.mx/",
        contact=openapi.Contact(email="lourdes.2080.institucional@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,

)

#app_name = "contratos"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('api/', include('users.api.router')),
    path('api/', include(router_user.urls)),
    path('api/', include(router_dependencia.urls)),
    path('api/', include(router_contrato.urls)),
    path('api/', include(router_contratooperativo.urls)),
    #path('api/generar_pdf/<int:contrato_id>/', views.generate_PDF, name='generar_pdf'),
    path('api/', include('contratos.urls')),
    path('api/', include('contratosoperativos.urls')),
    path('api/', include(router_fichatecnica.urls)),
     
]

#código para servir archivos de media durante el desarrollo: 
#Esta configuración es para fines de desarrollo. En un entorno de producción, servirías archivos de media utilizando un servidor web o una solución de servicio de medios dedicada.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #medios

