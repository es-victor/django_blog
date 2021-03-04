from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_posted", "location")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author","content","created_on","post")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

# admin.site.register(Category)
# admin.site.register(Post)
# admin.site.register(Comment)
