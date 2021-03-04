from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        # return self.name
        return f"{self.name}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='posts')
    title = models.CharField(max_length=100)
    # content = models.TextField()
    likes = models.ManyToManyField(User, related_name="blog_posts")
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.TextField(max_length=50, default='Dar es Salaam')

    def __str__(self):
        # return self.title + '" --posted by-- "' + str(self.author)
        return f"{self.title},{self.author},{self.date_posted},{self.location}"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    def total_likes(self):
        return self.likes.count()
    # class Meta:
    #     ordering = ('-date_posted',)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250, )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return '"' + str(self.author) + '" --commented on-- "' + self.post.title[:40] + '" --  "' + self.content + '"'
        return f"{self.content},{self.author},{self.created_on}"


