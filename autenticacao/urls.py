from django.urls import path # para criar url tem que ter path
from . import views # da pasta que está vai importar o views

urlpatterns = [
    # path( url, funcao para açao, name [que não é obrigatório, apenas para organizaçao])
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('logar/', views.logar, name='logar'),
    path('sair/', views.sair, name='sair'),
]

