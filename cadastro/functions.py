from django.db.models import Q
from . import models

def get_entidades_pais(id_tipo_entidade):
    if id_tipo_entidade == 12 or id_tipo_entidade == 0 or id_tipo_entidade == 1 or id_tipo_entidade == 2:
        entidadespais = models.Entidade.objects.filter(
            Q(tipo_entidade=models.TipoEntidade.objects.get(pk=0))
            | Q(tipo_entidade=models.TipoEntidade.objects.get(pk=1))
            | Q(tipo_entidade=models.TipoEntidade.objects.get(pk=2)))
    else:
        entidadespais = models.Entidade.objects.filter(
            Q(tipo_entidade=models.TipoEntidade.objects.get(pk=0))
            | Q(tipo_entidade=models.TipoEntidade.objects.get(pk=1))
            | Q(tipo_entidade=models.TipoEntidade.objects.get(pk=2))
            | Q(tipo_entidade=models.TipoEntidade.objects.get(pk=12)))

    return entidadespais