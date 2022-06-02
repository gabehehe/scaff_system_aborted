from django.shortcuts import render

# Create your views here.
def index(request):
    template_name = 'fiscalizacao/index.html'
    return render(request,template_name)

def processos_andamento(request):
    template_name = 'fiscalizacao/processos_andamento.html'
    return render(request,template_name)

def inicio_processo(request):
    template_name = 'fiscalizacao/form_inicio_processo.html'
    return render(request,template_name)

