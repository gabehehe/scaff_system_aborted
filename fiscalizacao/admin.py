from django.contrib import admin

from .models import Processo, TipoArtefato, TipoPenalidade, TipoRegistro, Penalidade

class ProcessoAdmin(admin.ModelAdmin):
    list_display = ['nup', 'data_inicio', 'data_fim']
    search_fields = ['nup']

class TipoPenalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_penalidade']
    search_fields = ['nome_penalidade']

class TipoArtefatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_artefato', 'aplicabilidade']
    search_fields = ['nome_artefato']

class TipoRegistroAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_tipo_registro', 'descricao_tipo_registro']
    search_fields = ['nome_tipo_registro']

class PenalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'dt_inicio_penalidade', 'dt_fim_penalidade', 'observacao', 'autoridade_responsavel']
    search_fields = ['dt_inicio_penalidade', 'dt_fim_penalidade']

admin.site.register(Processo, ProcessoAdmin)
admin.site.register(TipoPenalidade, TipoPenalidadeAdmin)
admin.site.register(TipoArtefato, TipoArtefatoAdmin)
admin.site.register(TipoRegistro, TipoRegistroAdmin)
admin.site.register(Penalidade, PenalidadeAdmin)
