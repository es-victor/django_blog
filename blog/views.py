from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, CheckboxSelectMultiple
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.shortcuts import render, get_object_or_404
from datetime import time, date, datetime
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from . import forms
from .models import Post, Comment, Category
from .forms import NewCommentForm, NewPostForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )


def home(request):
    # dictionary to pass data(posts)

    search_post = request.GET.get('search')
    if search_post:
        context = {
            'posts': Post.objects.filter(Q(title__icontains=search_post) | Q(content__icontains=search_post)).order_by(
                '-date_posted'),
            'title': 'Home Page',
            'home': 'active',
        }
    else:
        context = {
            'posts': Post.objects.all().order_by('-date_posted'),
            'title': 'Home Page',
            'home': 'active',
        }
    return render(request, 'blog/home.html', context)


# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         liked = False
#         post.save()
#     else:
#         post.likes.add(request.user)
#         liked = True
#         post.save()
#
#     return JsonResponse({'liked': liked, 'count': post.total_likes()})
@login_required
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('postid')
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            user_liked = 'not_liked'
            count = post.total_likes()
            post.save()


        else:
            post.likes.add(request.user)
            user_liked = 'liked'
            count = post.total_likes()
            post.save()
        return JsonResponse({'user_liked': user_liked, 'count': str(count)}, status=200)
    return JsonResponse({}, status=500)


def is_like(request):
    if request.is_ajax and request.method == "GET":
        post_id = request.GET.get('postid')
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            user_liked = 'liked'
        else:
            user_liked = 'not_liked'
        return JsonResponse({'user_liked': user_liked, }, status=200)
    return JsonResponse({}, status=500)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    extra_context = {'home': 'active'}
    paginate_by = 4
    # search_post = request.GET.get('search')
    # if search_post:
    #     posts = Post.objects.filter(Q(title__icontains=search_post) & Q(content__icontains=search_post))
    # else:
    #     # If not searched, return default posts
    #     posts = Post.objects.all().order_by("-date_created")


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class CategoryPosts(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'category_posts'
    paginate_by = 4

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(categories=category).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number_of_likes = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = number_of_likes.total_likes()
        user_liked = 'no'
        if number_of_likes.likes.filter(id=self.request.user.id).exists():
            user_liked = 'yes'
        context['total_likes'] = total_likes
        context['user_liked'] = user_liked
        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-created_on')
        context['comments'] = comments_connected
        if self.request.user.is_authenticated:
            context['comment_form'] = NewCommentForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post=self.get_object())
        new_comment.save()
        new_comment.clean()
        return HttpResponseRedirect(request.path)
        # return render(self, request, *args, **kwargs) // THIS CAUSE FORM RESUBMISSION


# created a template with name = post_detail.html to match the default naming convetion so to remove the need for
# template_name as before(above)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = NewPostForm
    extra_context = {'post_create': 'active', 'submit_text': 'Post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = NewPostForm
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
