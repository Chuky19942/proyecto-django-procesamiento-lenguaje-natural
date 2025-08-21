from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from analisis import views

urlpatterns = [
    path('', include('analisis.urls')),
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("subir/", views.subir_archivo, name="subir_archivo"),
    path("generar_histograma/<int:pk>/", views.generar_histograma, name="generar_histograma"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
