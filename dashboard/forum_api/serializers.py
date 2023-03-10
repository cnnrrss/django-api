from .models import Post, User
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']


class PostSerializer(serializers.ModelSerializer):
    """
    serializer.Serializer requires a lot of duplication, user ModelSerializer instead
    """

    class Meta:
        model = Post
        fields = ['created', 'title', 'content', 'user', 'topic']
