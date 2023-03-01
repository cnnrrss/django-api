from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    path('posts/', views.PostList.as_view()),
    path('tags/', views.TagList.as_view()),
    path('topics/', views.TopicList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)