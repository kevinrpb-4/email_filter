from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import Empresa, Correo
from .serializers import EmpresaSerializer, CorreoSerializer

# Empresas: Listar y crear
class EmpresaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Empresa.objects.all().order_by('nombre')
    serializer_class = EmpresaSerializer


# Correos: Listar (si hay filtros) y crear en masa
class CorreoListCreateAPIView(generics.GenericAPIView):
    """
    GET: Lista correos si se pasa al menos un filtro (si no hay filtros regresa lista vacía).
    POST: Permite crear uno o muchos correos (envío masivo).
          - Si alguna entrada falla la validación, se devuelve error con detalles.
    """
    serializer_class = CorreoSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Correo.objects.all().order_by('-fecha')
        # Obtener filtros simples desde query params
        params = self.request.query_params
        # filtros admitidos
        emisor = params.get('emisor')
        destinatario = params.get('destinatario')
        empresa = params.get('empresa')  # id de la empresa
        fecha = params.get('fecha')      # YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS
        contenido = params.get('contenido')

        # Si no hay ningún filtro, devolvemos queryset vacío (regla del ejercicio)
        if not any([emisor, destinatario, empresa, fecha, contenido]):
            return qs.none()

        if emisor:
            qs = qs.filter(emisor__icontains=emisor)
        if destinatario:
            qs = qs.filter(destinatario__icontains=destinatario)
        if empresa:
            qs = qs.filter(empresa__id=empresa)
        if fecha:
            # intentamos filtrar por fecha (solo día si viene en formato YYYY-MM-DD)
            qs = qs.filter(fecha__date=fecha)  # si el campo fecha es datetime
        if contenido:
            qs = qs.filter(contenido__icontains=contenido)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Espera un objeto o una lista de objetos.
        Validaciones:
         - La empresa debe existir (PrimaryKeyRelatedField lo maneja)
         - codigo_unico no duplicado (serializers lo maneja)
        """
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        # Si validación falla, DRF lanza excepción al llamar is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)

        # Guardado dentro de transacción para consistencia
        with transaction.atomic():
            instances = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Endpoint de búsqueda separada (requiere 'contenido' como filtro obligatorio)
class CorreoSearchAPIView(generics.GenericAPIView):
    serializer_class = CorreoSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = Correo.objects.all().order_by('-fecha')
        params = self.request.query_params
        contenido = params.get('contenido')
        if not contenido:
            # Regla del ejercicio: cuando se consuma sin filtro devolver lista vacía.
            return qs.none()

        emisor = params.get('emisor')
        destinatario = params.get('destinatario')
        empresa = params.get('empresa')
        fecha = params.get('fecha')

        qs = qs.filter(contenido__icontains=contenido)
        if emisor:
            qs = qs.filter(emisor__icontains=emisor)
        if destinatario:
            qs = qs.filter(destinatario__icontains=destinatario)
        if empresa:
            qs = qs.filter(empresa__id=empresa)
        if fecha:
            qs = qs.filter(fecha__date=fecha)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
