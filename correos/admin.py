from django.contrib import admin
from .models import Empresa, Correo

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'codigo', 'created_at')
    search_fields = ('nombre', 'codigo')

@admin.register(Correo)
class CorreoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_unico', 'emisor', 'destinatario', 'empresa', 'fecha')
    search_fields = ('codigo_unico', 'emisor', 'destinatario', 'contenido')
    list_filter = ('empresa',)
