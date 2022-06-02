from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('entidade/home', views.index, name='entidade/home'),
    path('entidade/cadastro', views.novaEntidade, name='entidade/cadastro'),

    path(r'^entidade/detalhes/(?P<pk>\d+)/', views.detalhes, name='entidade/detalhes'),

    path('entidade/lista',views.listaEntidades, name='entidade/lista'),
    url(r'^entidade/altera/(?P<pk>\d+)/',views.altera, name='entidade/altera'),

    path('entidade/gravaentidade',views.gravaEntidade, name='entidade/gravaentidade'),

    path('bbb', views.ajax, name='ajax'),



]