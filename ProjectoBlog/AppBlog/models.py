from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    imagen = models.ImageField(upload_to='avatares', null=True, blank = True)

    def __str__(self):
        return f"{settings.MEDIA_URL}{self.imagen}"
    
class Posts(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    imagenPost = models.ImageField(null=True, blank=True, upload_to="imagenes/")

    def __str__(self):
        return self.titulo
    

