from django.contrib import admin
from django.urls import path, include

# para as imagens
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),
    # string vazia para só digitar plataforma na url e ir
    path('', include('plataforma.urls')), 
]

# urlpatterns para as imagens (iterar ao vetor acima)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)