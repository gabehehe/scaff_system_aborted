from builtins import int, TypeError, ValueError

from django import forms

from . import models

class EntidadeForm(forms.ModelForm):
    class Meta:
        model = models.Entidade

        fields = [
            'tipo_entidade',
            'nome_entidade',
            'razao_social',
            'cnpj_entidade',
            'telefone_entidade',
            'email_entidade',
            'dt_credenciamento',
            'ativa',
        ]

    def clean_nome_entidade(self):
        return self.cleaned_data['nome_entidade'].upper()

    def clean_razao_social(self):
        return self.cleaned_data['razao_social'].upper()

    def clean_email_entidade(self):
        return self.cleaned_data['email_entidade'].lower()



class EntidadeVinculadaForm(forms.ModelForm):
    class Meta:
        model = models.EntidadeVinculada

        fields = [
            'entidade_propria',
            'dt_vinculacao',
        ]

class EntidadeVinSituacaoForm(forms.ModelForm):
    class Meta:
        model = models.EntidadeVinSituacao

        fields = [
            'situacao',
        ]




class EnderecoForm(forms.ModelForm):
    class Meta:
        model = models.Endereco

        fields = [
            'municipio_ibge',
            'cep',
            'logradouro',
            'bairro',
            'numero',
            'complemento',
            'latitude',
            'longitude',
        ]


    def clean_logradouro(self):
        return self.cleaned_data['logradouro'].upper()
    def clean_bairro(self):
        return self.cleaned_data['bairro'].upper()
    def clean_numero(self):
        return self.cleaned_data['numero'].upper()
    def clean_complemento(self):
        if self.cleaned_data['complemento'] is not None:
            return self.cleaned_data['complemento'].upper()



class MunicipioForm(forms.ModelForm):
    estado_ibge = models.EstadoIbge.objects.order_by('uf')
    class Meta:
        model = models.MunicipioIbge

        fields = [
            'estado_ibge',
        ]

class EntidadeEnderecoForm(forms.ModelForm):
    class Meta:
        model = models.EntidadeEndereco

        fields = [
            'tipo_endereco',
            'dt_criacao',
        ]


class PessoaForm(forms.ModelForm):
    class Meta:
        model = models.PessoaFisica

        fields = [
            'cpf_pessoa',
            'tipo_pessoa',
            'nome_pessoa',
        ]

    def clean_nome_pessoa(self):
        return self.cleaned_data['nome_pessoa'].upper()

class EntidadePessoaForm(forms.ModelForm):
    class Meta:
        model = models.EntidadePessoa

        fields = [
            'telefone_pessoa',
            'email_pessoa',
        ]

    def clean_email_pessoa(self):
        return self.cleaned_data['email_pessoa'].lower()

class SeiForm(forms.ModelForm):
    class Meta:
        model = models.Sei


        fields = [
            'nro_processo',
            'tipo_processo',
            'descricao',
        ]

    def clean_descricao(self):
        return self.cleaned_data['descricao'].upper()