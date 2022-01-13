from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # uma url dinamica para exibir imovel ao ser clicado
    path('imovel/<str:id>', views.imovel, name="imovel"),
]