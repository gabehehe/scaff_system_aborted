from django.urls import path
from django.conf.urls import url
''
from . import views

urlpatterns = [
    path('', views.authenticationUser, name='accounts/login'),
    path('accounts/home', views.logout_view, name='accounts/logout'),
]