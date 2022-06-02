from django.urls import path

from . import views

urlpatterns = [
    path('monitoramento/denuncia/home', views.denuncia_index, name='monitoramento/denuncia/home'),
    path('monitoramento/denuncia/denuncia-em-analise', views.denuncia_em_analise, name='monitoramento/denuncia/denuncia-em-analise'),
    path('monitoramento/analise', views.analise, name='analise'),

    path('monitoramento/ajax', views.ajax, name='ajax-monitoramento'),
]
