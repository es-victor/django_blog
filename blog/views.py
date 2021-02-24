from django.shortcuts import render, get_object_or_404
from datetime import time, date, datetime
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )


# def home(request):
#     # dictionary to pass data(posts)
#     context = {
#         'posts': Post.objects.all(),
#         'title': 'Home Page',
#         'home': 'active',
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    extra_context = {'home': 'active'}
    paginate_by = 4
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["home"] = "active" 
    #     return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


# created a template with name = post_detail.html to match the default naming convetion so to remove the need for
# template_name as before(above)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories']
    extra_context = {'post_create': 'active', 'submit_text': 'Post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories']
    extra_context = {'submit_text': 'Update'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    fields = ['title', 'content']
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {
        'title': 'About Page',
        'about': 'active',
    }
    return render(request, 'blog/about.html', context)
