from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context={
        'page_title':'Início'
    }
    return render(request, 'home.html', context)

def auditoria(request):
    return render(request, 'auditoria/home.html')

def fiscalizacao(request):
    return render(request, 'fiscalizacao/home.html')

def denuncias(request):
    return render(request, 'denuncias/home.html')

def fraudes(request):
    return render(request, 'fraudes/home.html')

def lista_negativa_agr(request):
    return render(request, 'fraudes/lista_negativa_agr.html')

def dossies(request):
    return render(request, 'fraudes/dossies.html')

def example(request):
    context = {
        'page_title': 'Exemplo'
    }
    return render(request, 'example.html', context)

