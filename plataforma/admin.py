from django.contrib import admin
# importar todas as tabelas criadas para cá. obs: poderia ser feita com * no lugar das tabelas
from .models import Imagem, Cidade, DiasVisita, Horario, Imovei, Visitas

# personaliza o imovei uma vez que está registrado
@admin.register(Imovei)
class ImoveiAdmin(admin.ModelAdmin):
    list_display = ('rua', 'valor', 'quartos', 'tamanho', 'cidade', 'tipo')
    list_editable = ('valor', 'tipo')
    list_filter = ('cidade', 'tipo')

# de fato, registrar na pagina (pensar em como fazer isso com o for depois)
admin.site.register(Imagem)
admin.site.register(Cidade)
admin.site.register(DiasVisita)
admin.site.register(Horario)
admin.site.register(Visitas)


