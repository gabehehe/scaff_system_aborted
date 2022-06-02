from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request, json
from . models import Ocorrencia, CaracteristicasFisicas, FormasDeteccao

# Create your views here.
def denuncia_index(request):
    template_name = 'denuncias/denuncia_index.html'
    context ={
        'page_title' : 'Denúncias',
    }
    return render(request,template_name, context)


def denuncia_em_analise(request):
    template_name = 'denuncias/denuncia_em_analise.html'
    return render(request,template_name)


def analise(request):
    template_name = 'denuncias/analise.html'


    return render(request, template_name)




def ajax(request):
    url_saf = "http://localhost:8002/saf/"
    url_certificates = 'http://localhost:8003/certificates/'
    if request.GET.get('action') == 'get_ocorrencia_saf':
        oconum = request.GET.get('oco_num')
        url_saf = url_saf+'oconum/'+oconum
        try:
            response = urllib.request.urlopen(url_saf)
            data = json.loads(response.read())
            return JsonResponse(data, safe=False) #safe = False permite retornar array json
        except:
            return JsonResponse({'message': 'Ocorreu um erro na requisição!'}, status=500)

    if request.GET.get('action') == 'get_certificates_cpf':
        cpf = request.GET.get('cpf')
        url_certificates = url_certificates+'cpf/'+cpf
        try:
            if not cpf:
                return JsonResponse({})
            response = urllib.request.urlopen(url_certificates)
            data = json.loads(response.read())
            return JsonResponse(data, safe=False)  # safe = False permite retornar array json
        except:
            return JsonResponse({'message': 'Ocorreu um erro na requisição!'}, status=500)

    if request.GET.get('action') == 'get_certificates_email':
        email = request.GET.get('email')
        url_certificates = url_certificates + 'email/' + email
        try:
            if not email:
                return JsonResponse({})
            response = urllib.request.urlopen(url_certificates)
            data = json.loads(response.read())
            return JsonResponse(data, safe=False)  # safe = False permite retornar array json
        except:
            return JsonResponse({'message': 'Ocorreu um erro na requisição!'}, status=500)


    if request.GET.get('action') == 'save_oco_base':
        jsonFront = json.loads(request.GET.get('json'))
        ocorrencia = Ocorrencia()

        print(jsonFront)

        for j in jsonFront:
            if type(jsonFront[j]) is not list:
                valor = jsonFront[j]
                if valor == 'false':
                    valor = False
                if valor == 'true':
                    valor = True
                setattr(ocorrencia, j, valor)
        ocorrencia.save()

        for j in jsonFront['caracteristicas']:
            caracterisca = CaracteristicasFisicas()
            caracterisca.ocorrencia = ocorrencia
            caracterisca.tipo = j['tipo']
            caracterisca.observado = j['observado']
            caracterisca.save()

        for j in jsonFront['formas_deteccao']:
            formasdeteccao = FormasDeteccao()
            formasdeteccao.ocorrencia = ocorrencia
            formasdeteccao.forma_deteccao = j['forma_deteccao']
            formasdeteccao.resultado = bool(j['resultado'])
            formasdeteccao.save()

        return HttpResponse()

    return JsonResponse({'message': 'Ocorreu um erro na requisição!'}, status=500)