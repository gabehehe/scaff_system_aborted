from django.urls import path

from . import views

urlpatterns = [
    path('fiscalizacao/home', views.index, name='fiscalizacao/home'),
    path('fiscalizacao/processos-andamento', views.processos_andamento, name='fiscalizacao/processos-andamento'),
    path('fiscalizacao/iniciar-processo', views.inicio_processo, name='fiscalizacao/iniciar-processo'),
]