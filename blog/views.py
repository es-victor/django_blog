from django.shortcuts import render
from datetime import time, date, datetime
from .models import Post


def home(request):
    # dictionary to pass data(posts)
    context = {
        'posts': Post.objects.all(),
        'title': 'Home Page',
        'home': 'active',
    }

    return render(request, 'blog/home.html', context)


def about(request):
    context = {
        'title': 'About Page',
        'about': 'active',
    }

    return render(request, 'blog/about.html', context)
