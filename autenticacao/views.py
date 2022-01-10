from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth # pra fazer a autenticação de login

def cadastro(request): # recebe a requisicao do usuario como parametro
    # se for acessado direto pela url
    if request.method == "GET":
        # se estiver logado, não pode voltar para o login pelo get
        if request.user.is_authenticated:
            return redirect('/')

        # retorna a propria pagina (como já tá escrito templates, o django já procura por padrao lá)
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        # pegando os valores
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # validações de campo

        # se o campo for vazio (incluindo espaços), dá um reload na pagina
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
            # exibe mensagem de alerta (requisição, tipo de alerta, mensagem que vai aparecer ao usuario)
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            
            # reload na pagina
            return redirect('/auth/cadastro')

        # ve se tem usuario igual cadastrado no banco
        user = User.objects.filter(username=username)

        # caso sim, reload na pagina
        if user.exists():
            # exibe mensagem 
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')

            # reload na pagina
            return redirect('/auth/cadastro') 
    

        # cadastrar no banco de dados e redirecionar login
        try:
            # é como se estivesse instanciando a classe
            user = User.objects.create_user(username = username,
                        email = email,
                        password = senha)

            # salva usuario
            user.save()

            # exibe mensagem
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')

            # redireciona para login
            return redirect('/auth/logar')
        except:
            # se der algum erro, exibe mensagem tambem
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')

            # e redireciona para cadastro
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        # se estiver logado, não pode voltar para o login pelo get
        if request.user.is_authenticated:
            return redirect('/')

        return render(request, 'logar.html')
    elif request.method == "POST":
        # capturar dados
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # fazer a autenticação de fato
        usuario = auth.authenticate(username = username, password = senha)
        
        # caso o usuario não exista
        if not usuario:
            # exibe mensagem de erro
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos!')
            # dá reload na pagina
            return redirect('/auth/logar')
        else: 
            # se tiver tudo certo, ele vai criar uma sessão para começar o login
            # os parametros são: a requisição e a variavel que guarda nome e senha
            auth.login(request, usuario)
            return redirect('/')


