"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from core import views
from accounts import views as e




urlpatterns = [

    path('', e.authenticationUser, name='login'),
    path('home/', views.home, name='home'),
    path('example/', views.example, name='example'),
    path('auditoria/', views.auditoria, name='auditoria'),
    path('', include('fiscalizacao.urls')),
    # modificado
    path('', include('monitoramento.urls')),
    #
    path('denuncias/', views.denuncias, name='denuncias'),
    path('fraudes/', views.fraudes, name='fraudes'),
    path('lista_negativa_agr/', views.lista_negativa_agr, name='lista_negativa_agr'),
    path('dossies/', views.dossies, name='dossies'),
    path('admin/', admin.site.urls),
    path('', include('cadastro.urls')),
    path('', include('accounts.urls'))
]


