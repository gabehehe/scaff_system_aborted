from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Denuncia


class AdminDenuncia(admin.ModelAdmin):
    list_display = ['canal_entrada', 'assunto', 'conclusao', 'data_fim', 'nup_fiscalizacao']
    search_fields = ['canal_entrada', 'assunto', 'conclusao', 'data_fim', 'nup_fiscalizacao']

admin.site.register(Denuncia, AdminDenuncia)
