from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView
from .models import Post


class BaseView(TemplateView):
    template_name = "base.html"


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить,
        model = Post
    # Поле, которое будет использоваться для сортировки объектов,
        ordering = 'post_pub_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
        template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
        context_object_name = 'posts_list'


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
