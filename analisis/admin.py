from django.contrib import admin
from .models import Archivo

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "archivo", "subido_en")
    search_fields = ("nombre", "archivo")
    list_filter = ("subido_en",)
