# articles/views.py

from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Importación de mixins
from .models import Article, Comment
from .forms import CommentForm, ArticleForm

class CommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def get_object(self, queryset=None):
        # Obtiene el artículo basado en el pk de la URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)

    def get(self, request, *args, **kwargs):
        # Asigna el objeto antes de manejar la solicitud
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añade el artículo al contexto
        context['article'] = self.get_object()
        context['comments'] = Comment.objects.filter(article=context['article'])  # Añade los comentarios
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.get_object()
        comment.author = self.request.user  # Asigna el autor autenticado
        comment.save()
        return redirect("article_detail", pk=self.get_object().pk)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar comentarios para cada artículo en el contexto
        for article in context['object_list']:
            article.comments = Comment.objects.filter(article=article)  # Obtener comentarios para cada artículo
        return context


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ArticleDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


class ArticleDetailDisplay(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Pasamos el formulario de comentarios al contexto
        context['comments'] = Comment.objects.filter(article=self.object)  # Pasamos los comentarios
        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # Vista para actualizar el artículo
    model = Article
    fields = ['title', 'body']
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # Vista para eliminar el artículo
    model = Article
    template_name = 'article_delete.html'  

    def get_success_url(self):
        return reverse('article_list')  # Redirige a la lista de artículos después de eliminar

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):  # Vista para crear un nuevo artículo
    model = Article
    template_name = 'article_new.html'
    form_class = ArticleForm  # Usamos el ArticleForm que incluye el campo image_url

    def form_valid(self, form):
        form.instance.author = self.request.user  # Asignamos el autor autenticado
        return super().form_valid(form)
    
# views para editar y borrar los comentarios
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']  # Solo permitimos editar el contenido del comentario
    template_name = 'comment_edit.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user  # Solo permite a los propietarios editar

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user  # Solo permite a los propietarios borrar

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.article.pk})
