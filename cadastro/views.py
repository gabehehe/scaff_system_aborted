from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from datetime import date
from django.contrib.auth.decorators import login_required
import urllib.request, json


from . import models
from . import  forms
from . import  functions

from . import models
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse


from . import models

from . import  forms

from . import models

# Create your views here.


def novaEntidade(request):
    print("novo")
    formEntidade = forms.EntidadeForm(request.POST or None)
    formEntVin = forms.EntidadeVinculadaForm(request.POST or None)
    formEntidadeVinSit = forms.EntidadeVinSituacaoForm(request.POST or None)

    context = {
        'form_entidade': formEntidade,
        'form_ent_vin': formEntVin,
        'form_ent_vin_sit': formEntidadeVinSit,
        'listTipoProcesso': models.TipoProcesso.objects.all,
        'list_estados_ibge': models.EstadoIbge.objects.all,
        'list_mun_ibge': models.MunicipioIbge.objects.all,
        'entidade_active': True,
        'tipo_formulario': "cadastro",
        'list_tipo_pessoa': models.TipoPessoa.objects.all,
    }


    if 'id_entidade_altera' in request.session:
        del request.session['id_entidade_altera']

    return render(request, "cadastro/entidade.html", context)

def altera(request, pk=None):
    print("altera")
    if pk:
        entidade = models.Entidade.objects.get(pk=pk)
        entidadesvinculadasPais = models.EntidadeVinculada.objects.filter(entidade_filha_id=entidade.id)
        entidadesvinculadasFilhas = models.EntidadeVinculada.objects.filter(entidade_propria_id=entidade.id)

        instance = get_object_or_404(models.Entidade, id=entidade.id)
        form_entidade = forms.EntidadeForm(request.POST or None, instance=instance)

        entidadespais = functions.get_entidades_pais(entidade.tipo_entidade.id)



        context = {
            'form_entidade': form_entidade,
            'entidade': entidade,
            'entidadesvinculadasPais': entidadesvinculadasPais,
            'entidadesvinculadasFilhas': entidadesvinculadasFilhas,
            'entidade_active': True,
            'listTipoProcesso': models.TipoProcesso.objects.all,
            'list_estados_ibge': models.EstadoIbge.objects.all,
            'list_mun_ibge': models.MunicipioIbge.objects.all,
            'tipo_formulario': "altera",
            'list_tipo_pessoa': models.TipoPessoa.objects.all,
            'entidadespais': entidadespais,
            'situacoes': models.Situacao.objects.all,
        }

        request.session['id_entidade_altera'] = pk

        return render(request, "cadastro/entidade.html", context)
    else:
        entidade = None

    context = {
        'entidade': entidade
    }

    return render(request, "cadastro/entidade.html", context)



def detalhes(request, pk=None):
    if pk:
        entidade = models.Entidade.objects.get(pk=pk)
        entidadesvinculadasPais = models.EntidadeVinculada.objects.filter(entidade_filha_id=entidade.id)
        entidadesvinculadasFilhas = models.EntidadeVinculada.objects.filter(entidade_propria_id=entidade.id)

        context = {
            'entidade': entidade,
            'entidadesvinculadasPais': entidadesvinculadasPais,
            'entidadesvinculadasFilhas': entidadesvinculadasFilhas,
        }

        return render(request, "cadastro/detalhes.html", context)



def ajax(request):
    if request.GET.get('action') == 'load_mun':
        id_estado_ibge = request.GET.get('estado_ibge')

        listmunicipios = models.MunicipioIbge.objects.filter(estado_ibge__id=id_estado_ibge).order_by('descricao_mun_ibge')

        context = {
            'municipios': listmunicipios,
        }
        return render(request, "cadastro/ajax/municipios_list.html", context)

    if request.GET.get('action') == 'get_processo':
        nroprocesso = request.GET.get('processo')
        listprocessos = models.Sei.objects.filter(nro_processo=nroprocesso)

        if listprocessos.count() > 0:  #len(listprocessos)
            sei = listprocessos[0]

            context = {
                'id_tipo_processo': sei.tipo_processo.id,
                'descricao_processo': sei.descricao,
            }
            return JsonResponse(context)


    if request.GET.get('action') == 'get_endereco':
        cep = request.GET.get('cep')
        url = "https://viacep.com.br/ws/"+cep+"/json/"

        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
        except:
            return HttpResponse()

        return JsonResponse(data)

    if request.GET.get('action') == 'novo_endereco':
        if 'id_entidade_endereco' in request.session:
            del request.session['id_entidade_endereco']

        formEndereco = forms.EnderecoForm(request.POST or None)
        formMun = forms.MunicipioForm(request.POST or None)
        formEntEnd = forms.EntidadeEnderecoForm(request.POST or None)

        context = {
            'form_endereco': formEndereco,
            'form_mun': formMun,
            'form_ent_end': formEntEnd,
        }
        return render(request, "cadastro/ajax/form_endereco.html", context)


    if request.GET.get('action') == 'altera_endereco':
        id_ee = request.GET.get('id_entidade_endereco')
        entidadeendereco = models.EntidadeEndereco.objects.get(pk=id_ee)
        entidadeendereco.tipo_endereco = request.GET.get('tipo_endereco')
        entidadeendereco.endereco.bairro = request.GET.get('bairro')
        entidadeendereco.endereco.cep = request.GET.get('cep')
        entidadeendereco.endereco.logradouro = request.GET.get('logradouro')
        entidadeendereco.endereco.numero = request.GET.get('numero')
        entidadeendereco.endereco.complemento = request.GET.get('complemento')
        entidadeendereco.endereco.latitude = request.GET.get('latitude')
        entidadeendereco.endereco.longitude = request.GET.get('longitude')
        entidadeendereco.endereco.municipio_ibge = models.MunicipioIbge.objects.get(pk=request.GET.get('municipio'))
        entidadeendereco.save()
        entidadeendereco.endereco.save()

        return HttpResponse()

    if request.GET.get('action') == 'exclui_endereco':
        id_entidade_endereco = request.GET.get('id_entidade_endereco')
        entidadeendereco = models.EntidadeEndereco.objects.get(pk=id_entidade_endereco)
        entidadeendereco.dt_extincao = date.today()
        entidadeendereco.save()
        return  HttpResponse()


  # ===================================================================
    if request.GET.get('action') == 'get_pessoa':
        cpfpessoa = request.GET.get('cpfpessoa')
        # idtipopessoa = request.GET.get('id_tipo_pessoa')

        listpessoas = models.PessoaFisica.objects.filter(cpf_pessoa=cpfpessoa)
        # listpessoas = listpessoas.filter(tipo_pessoa = models.TipoPessoa.objects.get(pk=idtipopessoa))

        if listpessoas.count() > 0:  # len(listprocessos)
            pessoafisica = listpessoas[0]
            context = {
                # 'id_tipo_pessoa': pessoafisica.tipo_pessoa.id,
                'nome_pessoa': pessoafisica.nome_pessoa,
            }
            return JsonResponse(context)


    if request.GET.get('action') == 'nova_pessoa':
        if 'id_entidade_pessoa' in request.session:
            del request.session['id_entidade_pessoa']

        formPessoa = forms.PessoaForm(request.POST or None)
        formEntPessoa = forms.EntidadePessoaForm(request.POST or None)

        context = {
            'form_pessoa': formPessoa,
            'form_ent_pessoa': formEntPessoa,
        }
        return render(request, "cadastro/ajax/form_pessoa.html", context)


    if request.GET.get('action') == 'altera_pessoa':
        id_ep = request.GET.get('id_entidade_pessoa')
        entidadepessoa = models.EntidadePessoa.objects.get(pk=id_ep)
        entidadepessoa.telefone_pessoa = request.GET.get('telefone')
        entidadepessoa.email_pessoa = request.GET.get('email')
        entidadepessoa.pessoa.cpf_pessoa = request.GET.get('cpf')
        entidadepessoa.pessoa.nome_pessoa = request.GET.get('nome')
        entidadepessoa.pessoa.tipo_pessoa = models.TipoPessoa.objects.get(pk=request.GET.get('id_tipo_pessoa'))
        entidadepessoa.save()
        entidadepessoa.pessoa.save()

        return HttpResponse();

    if request.GET.get('action') == 'exclui_pessoa':
        id_entidade_pessoa = request.GET.get('id_entidade_pessoa')
        entidadepessoa = models.EntidadePessoa.objects.get(pk=id_entidade_pessoa)
        entidadepessoa.dt_extincao = date.today()
        entidadepessoa.save()
        return  HttpResponse()



    #======================PROCESSOS=================================

    if request.GET.get('action') == 'novo_processo':
        form_sei = forms.SeiForm(request.POST or None)
        context = {
            'form_sei': form_sei,
        }
        return render(request, "cadastro/ajax/form_processo.html", context)

    if request.GET.get('action') == 'exclui_processo':
        id_sei = request.GET.get('id_sei')
        id_entidade = request.GET.get('id_entidade')

        entidade = models.Entidade.objects.get(pk=id_entidade)
        sei = models.Sei.objects.get(pk=id_sei)
        entidade.sei_set.remove(sei)


        return  HttpResponse()
#================================== VINCULAÇÃO ===============================
    if request.GET.get('action') == 'exclui_vinculacao':
        id_ev = request.GET.get('id_entidade_vinculada')
        entidadevinculada = models.EntidadeVinculada.objects.get(pk=id_ev)
        entidadevinculada.dt_extincao = date.today()
        entidadevinculada.save()

        return  HttpResponse()

    if request.GET.get('action') == 'altera_vinculacao':
        id_ev = request.GET.get('id_entidade_vinculada')
        entidadevinculada = models.EntidadeVinculada.objects.get(pk=id_ev)
        entidadevinculada.dt_vinculacao = request.GET.get('dt_vinculacao')

        for evs in entidadevinculada.entidadevinsituacao_set.all():
            if evs.dt_extincao is None:
                if evs.situacao.id != int(request.GET.get('id_situacao')):
                    evs.dt_extincao = date.today()
                    evs.save()
                    entidadevinculadasituacao = models.EntidadeVinSituacao()
                    entidadevinculadasituacao.dt_criacao = date.today()
                    entidadevinculadasituacao.entidade_vinculada = entidadevinculada
                    entidadevinculadasituacao.situacao = models.Situacao.objects.get(pk = request.GET.get('id_situacao'))
                    entidadevinculadasituacao.save()

        entidadevinculada.save()
        return HttpResponse()

    return HttpResponse()



@login_required
def listaEntidades(request):
    listEntidades = models.Entidade.objects.all
    context = {
        'entidades': listEntidades,
    }

    if request.method == 'POST':
        id = request.POST.get('id_entidade')
        print (id)

    return render(request, "cadastro/lista.html", context)







def index(request):
    ac1 = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=1))
    ac2 = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=2))
    ar = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=12))
    it = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=17))
    its = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=18))
    # pp = models.Entidade.objects.filter(tipo_entidade=models.TipoEntidade.objects.get(pk=19))
    print(ac1)


    context = {
        'page_title': 'Entidades',
        'qtdac1': ac1,
        'qtdac2': ac2,
        'qtdar': ar,
        'qtdit': it,
        'qtdits': its,
        'qtdpp': 0,

    }
    return render(request, "cadastro/index.html", context)


def gravaEntidade(request):
    instance_pessoa= None
    if 'id_entidade_altera' in request.session:
        instance_pessoa = get_object_or_404(models.Entidade, id=request.session['id_entidade_altera'])
        del request.session['id_entidade_altera']

    formEntidade = forms.EntidadeForm(request.POST or None, instance=instance_pessoa)
    formEntVin = forms.EntidadeVinculadaForm(request.POST or None)
    formEntidadeVinSit = forms.EntidadeVinSituacaoForm(request.POST or None)



    if formEntidade.is_valid():
        entidade = formEntidade.save(commit=False)
        print (entidade.id)

        if instance_pessoa == None and formEntidadeVinSit.is_valid() and formEntVin.is_valid():
            print("novo")
            entidade.save()
            entidadevinculada = formEntVin.save(commit=False)
            entidadevinculada.entidade_filha = entidade
            entidadevinculada.save()

            entidadevinsituacao = formEntidadeVinSit.save(commit=False)
            entidadevinsituacao.dt_criacao = entidadevinculada.dt_vinculacao
            entidadevinsituacao.entidade_vinculada = entidadevinculada
            entidadevinsituacao.save()
        elif instance_pessoa != None:
            entidade.save()
            for v in request.POST.getlist('vinculacoes'):
                for vinretorno in json.loads(v):
                    entidade_pai = models.Entidade.objects.get(pk=vinretorno['id'])
                    entidadevinculada = models.EntidadeVinculada()
                    entidadevinculada.entidade_propria = entidade_pai
                    entidadevinculada.entidade_filha = entidade
                    entidadevinculada.dt_vinculacao = vinretorno['dt_vinculacao']
                    entidadevinculada.save()

                    entidadevinsituacao = models.EntidadeVinSituacao()
                    entidadevinsituacao.dt_criacao = date.today()
                    entidadevinsituacao.entidade_vinculada = entidadevinculada
                    entidadevinsituacao.situacao = models.Situacao.objects.get(pk=vinretorno['id_situacao'])
                    entidadevinsituacao.save()
        else:
            print("erro")
            return HttpResponse();



        for t in request.POST.getlist('processos'):
            seilist = json.loads(t)
            for seiretorno in seilist:
                listprocessos = models.Sei.objects.filter(nro_processo=seiretorno['nro'])
                sei = models.Sei()
                if listprocessos.count() > 0:
                    sei.id = listprocessos[0].id
                sei.descricao = seiretorno['descricao']
                sei.nro_processo = seiretorno['nro']
                sei.tipo_processo = models.TipoProcesso.objects.get(pk=seiretorno['id_tipo_processo'])
                sei.save()
                sei.entidades.add(entidade)

        for pes in request.POST.getlist('pessoas'):
            peslist = json.loads(pes)
            for pessoa in peslist:
                listpessoas = models.PessoaFisica.objects.filter(cpf_pessoa=pessoa['cpf'])\
                    .filter(tipo_pessoa = models.TipoPessoa.objects.get(pk=pessoa['id_tipo_pessoa']))

                print (listpessoas)

                pessoafisica = models.PessoaFisica()
                if listpessoas.count() > 0:
                    pessoafisica.id = listpessoas[0].id
                pessoafisica.nome_pessoa = pessoa['nome']
                pessoafisica.cpf_pessoa = pessoa['cpf']
                pessoafisica.tipo_pessoa = models.TipoPessoa.objects.get(pk=pessoa['id_tipo_pessoa'])
                pessoafisica.save()
                entidadepessoa = models.EntidadePessoa()
                entidadepessoa.entidade = entidade
                entidadepessoa.pessoa = pessoafisica
                entidadepessoa.telefone = pessoa['telefone']
                entidadepessoa.email = pessoa['email']
                entidadepessoa.save()

        for ender in request.POST.getlist('enderecos'):
            endlist = json.loads(ender)
            for end in endlist:
                endereco = models.Endereco()
                endereco.cep = end['cep']
                endereco.logradouro = end['logradouro']
                endereco.bairro = end['bairro']
                endereco.numero = end['numero']
                endereco.complemento = end['complemento']
                endereco.latitude = end['latitude']
                endereco.longitude = end['longitude']
                endereco.municipio_ibge = models.MunicipioIbge.objects.get(pk=end['id_mun'])
                endereco.save()
                entidadeendereco = models.EntidadeEndereco()
                entidadeendereco.endereco = endereco
                entidadeendereco.entidade = entidade
                entidadeendereco.tipo_endereco = end['tipo_endereco']
                entidadeendereco.save()


    return HttpResponse()



