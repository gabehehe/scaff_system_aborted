from builtins import Exception

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from . import models
from . import enums

def authenticationUser(request):
    print(request.user)
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if(user is not None):
            try:
                if user.type_user.id == enums.TypeUsersEnum.VISITANTE.value:
                    mensagem = 'Usuário sem permissão!'
                else:
                    login(request, user)
                    return render(request, "home.html")
            except Exception as e:
                print(e)
                mensagem = 'Usuário não encontrado!'
        else:
            mensagem = 'Login ou senha incorretos!'


        context = {'mensagem': mensagem}
        return render(request, "accounts/login.html", context)
    else:
        if request.user.is_authenticated:
            return render(request, "home.html")


    return render(request,"accounts/login.html")


def login_page(request):
    return render(request, "accounts/login.html")

def logout_view(request):
    print("logout")
    logout(request)
    return authenticationUser(request)
