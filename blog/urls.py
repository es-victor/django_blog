from django.urls import path
from . import views
from .views import CategoryPosts, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    UserPostListView

urlpatterns = [
    path('', views.home, name="blog-home"),
    # path('', PostListView.as_view(), name="blog-home"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    # path('post/<int:pk>/', views.post_detail, name="post-detail"),
    # path('post/<int:pk>/comment/', PostCommentView.as_view(), name="post-comment"),
    # path('like/<int:pk>', LikeView, name="like_post"),
    path('like/', views.like, name="like_post"),
    path('isliked/', views.is_like, name="is_liked"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('category/<str:name>', CategoryPosts.as_view(), name="category-posts"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('about/', views.about, name="blog-about"),

]
