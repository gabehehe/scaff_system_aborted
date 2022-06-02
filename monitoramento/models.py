from django.db import models

# Create your models here.

from django.db import models


class PesquisaManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            nup__icontains=query
        )

class Denuncia(models.Model):
    canal_entrada = models.CharField("Canal de entrada da denúncia", max_length=100)
    assunto = models.CharField("Assunto da denúncia", max_length=100)
    transcricao = models.CharField("Transcrição da denúncia", max_length=10000)
    data_entrada = models.DateField("Data de recebimento da denúncia")
    data_fim = models.DateField("Data término da análise", null=True, blank=True)
    conclusao = models.CharField("Conclusão da análise da denúncia", max_length=1000, blank=True)
    modificado_em = models.DateTimeField("Data de Modificação", auto_now=True)
    nup_fiscalizacao = models.CharField("Processo de fiscalização gerado", max_length=17, blank=True)
    slug = models.SlugField("Link")


    objects = PesquisaManager()

    def __str__(self):
        return self.assunto



class Ocorrencia(models.Model):
    oco_num = models.CharField(max_length=255)
    responsavel_registro = models.CharField(max_length=255, null=True, blank=True)
    cpf_responsavel_registro = models.CharField(max_length=255, null=True, blank=True)
    data_cadastro = models.DateTimeField(null=True, blank=True)
    data_oco = models.DateTimeField(null=True, blank=True)
    tipo_certificado = models.CharField(max_length=255, null=True, blank=True)
    tipo_ocorrencia = models.BooleanField(null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    descricao_oco = models.CharField(max_length=255, null=True, blank=True)
    justificativa_marcador = models.CharField(max_length=255, null=True, blank=True)
    codinome = models.CharField(max_length=255, null=True, blank=True)
    autoridade_certificadora = models.CharField(max_length=255, null=True, blank=True)
    autoridade_registro = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.CharField(max_length=255, null=True, blank=True)
    marcador = models.CharField(max_length=255, null=True, blank=True)
    marcador_atribuido = models.CharField(max_length=255, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    representa_pj = models.BooleanField(null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=255, null=True, blank=True)
    infoseg = models.CharField(max_length=255, null=True, blank=True)
    etitulo = models.CharField(max_length=255, null=True, blank=True)
    redesociais = models.CharField(max_length=255, null=True, blank=True)
    cpf_agr = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.oco_num

class CaracteristicasFisicas(models.Model):
    tipo = models.CharField(max_length=255)
    observado = models.CharField(max_length=255)

    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name="caracteristicas")

    objects = models.Manager()
    def __str__(self):
        return self.tipo

class FormasDeteccao(models.Model):
    forma_deteccao = models.CharField(max_length=255)
    resultado = models.BooleanField(null=True, blank=True)

    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name="formas_deteccao")

    objects = models.Manager()
    def __str__(self):
        return self.forma_deteccao