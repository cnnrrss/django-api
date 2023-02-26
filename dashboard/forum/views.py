# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie
from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Post


@api_view(['GET', 'POST'])
def post_list(request):
    """
    List all code posts, or create a new post.
    """
    if request.method == 'GET':
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class PostView(views.APIView):
#     # Cache page for the requested url
#     # With cookie: cache requested url for each user for 2 hours
#     @method_decorator(cache_page(60*60*2))
#     @method_decorator(vary_on_cookie)
#     def get(self):
#         queryset = Post.objects.all()
#         return Response(content)