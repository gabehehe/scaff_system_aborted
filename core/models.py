from django.db import models

class ProcessoManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            nup__icontains=query
        )

class EntidadeManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            cnpj__icontains=query
        )

class TipoEntidadeManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            nome_tipo__icontains=query
        )
# class Andamento(models.Model):
#     lancamento = models.CharField()
#     data_registro = models.DateField()
#     responsavel = models.IntegerField()
#     tipo_andamento = models.IntegerField()
#     tipo_registro = models.IntegerField()

# class Artefato(models.Model):
#     nome = models.CharField()
#     descricao = models.CharField()
#     tipo_artefato = models.IntegerField()

class Processo(models.Model):
    nup = models.CharField(
        "NUP",
        max_length=17
    )
    entidade_fiscalizada_cod = models.IntegerField(
        "Entidade",
        blank=True,
        null=True
    )
    entidade_vinculada_cod = models.IntegerField(
        "Entidade de Vinculação",
        blank=True,
        null=True
    )
    situacao_processo = models.IntegerField(
        "Status do Processo",
        blank=False,
        null=False,
        default=1
    )
    data_inicio = models.DateField(
        "Data Início",
        blank=False,
        null=False
    )
    data_fim = models.DateField(
        "Data Fim",
        blank=True,
        null=True
    )
    criado_em = models.DateTimeField(
        "Data de Criação",
        auto_now_add=True
    )
    modificado_em = models.DateTimeField(
        "Data de Modificação",
        auto_now=True
    )
    sobrestado_inicio = models.DateField(
        "Sobrestado em",
        blank=True,
        null=True
    )
    sobrestado_fim = models.DateField(
        "Fim Sobrestado",
        blank=True,
        null=True
    )
    processo_slug = models.SlugField("processo")

    processo_objeto = ProcessoManager()

    def __str__(self):
        return self.nup

class Entidade(models.Model):
    nome = models.CharField(
        "Nome da Entidade",
        max_length=255,
        null=False,
        blank=False
    )
    cnpj = models.CharField(
        "CNPJ",
        max_length=14,
        null=False,
        blank=False
    )
    endereco = models.CharField(
        "Endereço",
        max_length=255,
        null=False,
        blank=False
    )
    razao_social = models.CharField(
        "Razão Social",
        max_length=255,
        null=True,
        blank=True
    )
    email = models.CharField(
        "E-mail",
        max_length=80,
        null=False,
        blank=False
    )

    entidade_pai = models.IntegerField(
        "Entidade de Vinculação",
        null=True,
        blank=True
    )
    entidade_objeto = EntidadeManager()

    def __str__(self):
        return self.cnpj

class TipoEntidade(models.Model):
    nome_tipo = models.CharField(
        "Tipo Entidade",
        max_length=30,
        null=False,
        blank=False
    )

    descricao_tipo = models.CharField(
        "Descrição",
        max_length=100,
        null=True,
        blank=True
    )

    tipo_entidade_objeto = TipoEntidadeManager()

    def __str__(self):
        return self.nome_tipo