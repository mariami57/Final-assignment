from rest_framework import serializers

from accounts.models import Profile
from books.models import Book
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'url']

    def get_url(self, obj):
        return f'/posts/{obj.id}/details/'


class BookSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'url']

    def get_url(self, obj):
        return f'/reviews/book/{obj.id}/reviews/'

class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = ['id', 'username', 'url']

    def get_url(self, obj):
        return f'/accounts/profile/{obj.id}/profile-details/'



