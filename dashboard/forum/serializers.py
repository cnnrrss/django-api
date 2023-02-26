from .models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """
    serializer.Serializer requires a lot of duplication, user ModelSerializer instead
    """

    class Meta:
        model = Post
        fields = ['created', 'title', 'content', 'user', 'topic']
