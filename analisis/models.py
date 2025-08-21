from django.db import models

class Archivo(models.Model):
    archivo = models.FileField(upload_to="archivos/")
    nombre = models.CharField(max_length=255, blank=True)
    subido_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre or self.archivo.name
