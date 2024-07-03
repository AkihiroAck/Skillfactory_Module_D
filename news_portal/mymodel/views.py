from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filter import ProductFilter
from django.urls import reverse_lazy
from .forms import PostForm

# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-creation_time'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostListSearch(ListView):
    model = Post
    ordering = '-creation_time'
    template_name = 'post_list_search.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['categories'] = post.category.all()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True  # Вызывает PermissionDenied вместо перенаправления на страницу логина
    permission_required = 'mymodel.add_post'  # Указываем право
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True  # Вызывает PermissionDenied вместо перенаправления на страницу логина
    permission_required = 'mymodel.change_post'  # Указываем право
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True  # Вызывает PermissionDenied вместо перенаправления на страницу логина
    permission_required = 'mymodel.delete_post'  # Указываем право
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
