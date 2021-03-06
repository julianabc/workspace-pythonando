from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cidade, Imovei, Visitas # para poder apresentar em home
from django.shortcuts import get_object_or_404

# sempre que tiver essa @ significa que o metodo só funciona com o login feito
# significa que caso não esteja logado, redireciona para a pagina de logar
@login_required(login_url='/auth/logar')
def home(request):
    # pegar os dados que veem da requisição (trabalhar com o modal)
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo')

    # trazer os dados para a pagina
    imoveis = Imovei.objects.all()
    cidades = Cidade.objects.all()

    # se algo foi passado por get... 
    if preco_minimo or preco_maximo or cidade or tipo:

        # verifica pois pode ser que só tenha sido utilizado o filtro para um dos campos
        if not preco_minimo:
            preco_minimo = 0
        if not preco_maximo:
            preco_maximo = 999999999
        if not tipo:
            tipo = ['A', 'C']

        # filtro para todos os valores que foram passados por get
        imoveis = Imovei.objects.filter(valor__gte=preco_minimo)\
        .filter(valor__lte=preco_maximo)\
        .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
    else:
        # se não tem filtro, passa todos os imoveis
        imoveis = Imovei.objects.all()

        # obs: mexer depois para a filtragem passar o valor zero pois tá sempre indo ou franca ou ribeirao
    # esse novo parametro envia imoveis para dentro de home
    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})



def imovel(request, id):
    # busca no banco de dados o imovel igual a id
    # caso não encontre, dá um erro 404
    imovel = get_object_or_404(Imovei, id=id)

    # mostra na tela 2 imoveis na mesma cidade e exclui o que já está sendo visitado
    sugestoes = Imovei.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]

    # renderizar pagina
    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes, 'id': id})


def agendar_visitas(request):
    # pegar dados importantes para agendar a visita
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')
    
    # criar visitas - instanciar essa classe
    visita = Visitas(
        imovel_id = id_imovel,
        usuario = usuario,
        dia = dia,
        horario = horario
    )

    # efetivar no banco de dados
    visita.save()

    # redirecionar para a pagina de agendamentos
    return redirect('/agendamentos')

# mostrar as visitas agendadas
def agendamentos(request):
    # traz apenas as visitas do usuario logado
    visitas = Visitas.objects.filter(usuario=request.user)

    # renderiza para a pagina que está
    return render(request, "agendamentos.html", {'visitas': visitas})


# metodo para cancelar agendamento
def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id) # busca visita agendada ou retorna erro
    visitas.status = "C" # modifica o status para cancelado
    visitas.save() # salva
    return redirect('/agendamentos') # redireciona para a pagina de agendamentos