# RUTA COMPLETA: C:\Cursos\Python\email_filter\correos\serializers.py
# NUEVO

from rest_framework import serializers
from .models import Empresa, Correo

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'codigo', 'descripcion', 'created_at']
        read_only_fields = ['id', 'created_at']

class CorreoSerializer(serializers.ModelSerializer):
    # empresa se representa por su id (PrimaryKey)
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())

    class Meta:
        model = Correo
        fields = [
            'id',
            'destinatario',
            'emisor',
            'fecha',
            'empresa',
            'codigo_unico',
            'contenido',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_contenido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El contenido es obligatorio y no puede estar vacío.")
        return value

    def validate(self, data):
        # Validación extra: la empresa debe existir (PrimaryKeyRelatedField ya lo verifica)
        # Además: asegurar que codigo_unico no exista (unique=True en el modelo, pero para mensajes más claros)
        codigo = data.get('codigo_unico')
        instance = getattr(self, 'instance', None)
        qs = Correo.objects.filter(codigo_unico__iexact=codigo)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"codigo_unico": "Ya existe un correo con este codigo_unico."})
        return data
