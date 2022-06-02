from django.db import models
from cadastro.models import Entidade

class ProcessoManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            nup__icontains=query
        )

class Processo(models.Model):
    nup = models.CharField(
        "NUP",
        max_length=17)
    entidade_fiscalizada_cod = models.ForeignKey(
        Entidade,
        on_delete=models.CASCADE)
    # entidade_fiscalizada_nome = models.CharField("Entidade", max_length=100)
    entidade_vinculada_cod = models.IntegerField(
        "Entidade Vinculada"
    )
    situacao_processo = models.IntegerField(
        "Status do Processo"
    )
    data_inicio = models.DateField(
        "Data Início"
    )
    data_fim = models.DateField(
        "Data Fim",
        blank=True
    )
    criado_em = models.DateTimeField(
        "Data de Criação",
        auto_now_add=True
    )
    modificado_em = models.DateTimeField(
        "Data de Modificação",
        auto_now=True
    )
    slug = models.SlugField("Link")

    objects = ProcessoManager()

    def __str__(self):
        return self.nup

class TipoPenalidadeManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            nome_penalidade__icontains=query
        )

class TipoPenalidade(models.Model):
    nome_penalidade = models.CharField(
        "Penalidade",
        max_length=30,
        blank=False,
        null=False
    )
    descricao_penalidade = models.CharField(
        "Descrição",
        max_length=255,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.nome_penalidade

class Penalidade(models.Model):
    dt_inicio_penalidade = models.DateField(
        "Data Início Penalidade",
        null=False,
        blank=False,
    )
    dt_fim_penalidade = models.DateField(
        "Data Fim Penalidade",
        null=True,
        blank=True
    )
    observacao = models.TextField(
        "Observações",
        null=True,
        blank=True
    )
    autoridade_responsavel = models.CharField(
        "Autoridade Responsável",
        max_length=100,
        null=False,
        blank=False
    )
    tipo_penalidade = models.ForeignKey(
        TipoPenalidade,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

class TipoRegistro(models.Model):
    nome_tipo_registro = models.CharField(
        "Tipo Registro",
        max_length=50,
        blank=False,
        null=False
    )
    descricao_tipo_registro = models.CharField(
        "Descrição",
        max_length=100,
        blank=True,
        null=True
    )

class TipoArtefato(models.Model):
    nome_artefato = models.CharField(
        "Tipo de Artefato",
        max_length=100,
        blank=False,
        null=False
    )
    aplicabilidade = models.CharField(
        "Aplicabilidade do artefato",
        max_length=255,
        blank=True,
        null=True
    )

class Artefato(models.Model):
    data_producao = models.DateTimeField(
        "Data de Produção",
        blank=False,
        null=False
    )
    responsavel = models.CharField(
        "Nome do Responsável",
        max_length=100,
        blank=False,
        null=False
    )
    tipo_artefato = models.ForeignKey(
        TipoArtefato,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

class TipoAndamento(models.Model):
    nome_tipo_andamento = models.CharField(
        "Tipo de andamento",
        max_length=50,
        null=False,
        blank=False
    )

class Andamento(models.Model):
    data_registro = models.DateTimeField(
        "Data do Registro",
        null=False,
        blank=False
    )
    observacao = models.TextField(
        "Observação",
        null=True,
        blank=True
    )
    tipo_andamento = models.ForeignKey(
        TipoAndamento,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    artefato = models.ForeignKey(
        Artefato,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    tipo_registro = models.ForeignKey(
        TipoRegistro,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    penalidade = models.ForeignKey(
        Penalidade,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )