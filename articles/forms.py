# articles/forms.py
from django import forms
from .models import Comment, Article

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)  # Solo mostramos el campo de comentario

# Formulario para los artículos
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image_url']