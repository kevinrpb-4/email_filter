from django.urls import path
from .views import (
    EmpresaListCreateAPIView,
    CorreoListCreateAPIView,
    CorreoSearchAPIView,
)

urlpatterns = [
    path('api/empresas/', EmpresaListCreateAPIView.as_view(), name='empresa-list-create'),
    path('api/correos/', CorreoListCreateAPIView.as_view(), name='correo-list-create'),
    path('api/correos/buscar/', CorreoSearchAPIView.as_view(), name='correo-search'),
]
