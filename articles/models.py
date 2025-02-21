# articles/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=255) # titulo maximo de 255 caracteres
    body = models.TextField() # entrada del contenido
    date = models.DateTimeField(auto_now_add=True) # agrega la fecha automaticamente
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    image_url = models.URLField(max_length=500, blank=True, null=True)  # Campo para la URL de la imagen
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    article = models.ForeignKey (Article,
            on_delete=models.CASCADE,
    )
    comment = models.CharField(
        max_length =140
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return self.comment
    
    def get_absolute_url (self):
        return reverse("article_list" )