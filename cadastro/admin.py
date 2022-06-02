from django.contrib import admin

from .models import Entidade, TipoEntidade, EstadoIbge, MunicipioIbge, PessoaFisica, EntidadeVinculada, Oid

class EntidadeAdmin(admin.ModelAdmin):
    list_display = ['nome_entidade', 'razao_social', 'tipo_entidade']
    search_fields = ['nup']

admin.site.register(Entidade, EntidadeAdmin)
admin.site.register(TipoEntidade)
admin.site.register(MunicipioIbge)
admin.site.register(EstadoIbge)
admin.site.register(PessoaFisica)
admin.site.register(EntidadeVinculada)
admin.site.register(Oid)
