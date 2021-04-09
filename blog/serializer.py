from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Post
from users.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'image']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'is_staff']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'date_posted']
        depth = 2
