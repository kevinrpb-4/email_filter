# RUTA COMPLETA: C:\Cursos\Python\email_filter\correos\models.py
# NUEVO

from django.db import models

class Empresa(models.Model):
    """
    Catálogo de empresas emisoras parametrizadas por el cliente.
    """
    nombre = models.CharField(max_length=150, unique=True)
    codigo = models.CharField(max_length=50, unique=True)  # código interno de la empresa
    descripcion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Correo(models.Model):
    """
    Registro de un correo analizado.
    Requerimientos:
      - destinatario
      - emisor
      - fecha
      - empresa (FK a Empresa)
      - codigo_unico (único por proveedor)
      - contenido
    """
    destinatario = models.CharField(max_length=254)
    emisor = models.CharField(max_length=254)
    fecha = models.DateTimeField()  # fecha y hora del correo
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='correos')
    codigo_unico = models.CharField(max_length=200, unique=True)  # clave única por proveedor SMTP
    contenido = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Correo"
        verbose_name_plural = "Correos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Correo {self.codigo_unico} de {self.emisor} -> {self.destinatario}"
