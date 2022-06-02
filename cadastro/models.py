from django.db import models

# Create your models here.
from datetime import datetime


# Create your models here.

class TipoEntidade(models.Model):

    tipo_descricao = models.CharField(max_length=255, blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.tipo_descricao

class Entidade(models.Model):

    tipo_entidade = models.ForeignKey(TipoEntidade, on_delete=models.CASCADE)

    razao_social = models.CharField("Razão Social", max_length=255, blank=False, null=True)

    nome_entidade= models.CharField(max_length=255, blank=False, null=True)

    cnpj_entidade = models.CharField(max_length=14, null=False, blank=False)

    telefone_entidade = models.CharField(max_length=50, null=True)

    email_entidade = models.CharField(max_length=255, null=True)

    dt_credenciamento = models.DateTimeField(default=datetime.now, null=True)

    ativa = models.BooleanField(default=True, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.nome_entidade


class EstadoIbge(models.Model):

    descricao_estado = models.CharField(
        max_length=255
    )

    uf = models.CharField(
        max_length = 3
    )

    objects = models.Manager()

    def __str__(self):
        return self.uf



class MunicipioIbge(models.Model):

    estado_ibge = models.ForeignKey(EstadoIbge, on_delete=models.CASCADE, verbose_name="UF")

    descricao_mun_ibge = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.descricao_mun_ibge






class Endereco(models.Model):

    municipio_ibge = models.ForeignKey(MunicipioIbge, on_delete=models.CASCADE, verbose_name="Município")

    cep = models.CharField(max_length=8,null=True)

    logradouro = models.CharField(max_length=255,null=True)

    bairro = models.CharField(max_length=255,null=True)

    numero = models.CharField(max_length=255, null=True)

    complemento = models.CharField(max_length=255,null=True, blank=True)

    latitude = models.CharField(max_length=255, null=True)

    longitude = models.CharField(max_length=255, null=True)

    objects = models.Manager()





class EntidadeEndereco(models.Model):
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    tipo_endereco = models.CharField(max_length=255, null=True)

    dt_criacao = models.DateTimeField(default=datetime.now, null=True)

    dt_extincao = models.DateTimeField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.tipo_endereco





class Oid(models.Model):

    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    descricao_oid = models.CharField(max_length=255, null=True)

    oid = models.CharField(max_length=255, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.descricao_oid


class TipoPessoa(models.Model):
    descricao_pessoa = models.CharField(max_length=255, blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.descricao_pessoa


class PessoaFisica(models.Model):

    nome_pessoa = models.CharField(max_length=255, null=True, blank=False)

    cpf_pessoa = models.CharField(max_length=11, null=True)

    tipo_pessoa = models.ForeignKey(TipoPessoa, on_delete=models.CASCADE)

    objects = models.Manager()



class EntidadePessoa(models.Model):

    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    pessoa = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)

    telefone_pessoa = models.CharField(max_length=50, null=True)

    email_pessoa = models.CharField(max_length=255, null=True)

    dt_criacao = models.DateTimeField(default=datetime.now, null=True)

    dt_extincao = models.DateTimeField(null=True)

    objects = models.Manager()




#class EntidadeSei(models.Model):



class TipoProcesso(models.Model):
    descricao_processo = models.CharField(max_length=255, blank=False, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.descricao_processo


class Sei(models.Model):

    entidades = models.ManyToManyField(Entidade)

    descricao = models.TextField(null=True)

    nro_processo = models.CharField(max_length=255)

    dt_inclusao = models.DateTimeField(default=datetime.now, null=True)

    tipo_processo = models.ForeignKey(TipoProcesso, on_delete=models.CASCADE)

    objects = models.Manager()




class EntidadeVinculada(models.Model):

    entidade_propria = models.ForeignKey(Entidade, related_name='entidade_propria', on_delete=models.CASCADE, verbose_name="Entidade pai")

    entidade_filha = models.ForeignKey(Entidade, related_name='entidade_filha', on_delete=models.CASCADE, verbose_name="Entidade filha")

    dt_vinculacao = models.DateTimeField(null=True)

    dt_extincao = models.DateTimeField(null=True)

    objects = models.Manager()


class Situacao(models.Model):

    descricao_situacao = models.CharField(
        max_length=255
    )

    objects = models.Manager()

    def __str__(self):
        return self.descricao_situacao




class EntidadeVinSituacao(models.Model):

    entidade_vinculada = models.ForeignKey(EntidadeVinculada, on_delete=models.CASCADE)

    situacao = models.ForeignKey(Situacao, on_delete=models.CASCADE)

    dt_criacao = models.DateTimeField(null=True)

    dt_extincao = models.DateTimeField(null=True)

    objects = models.Manager()




