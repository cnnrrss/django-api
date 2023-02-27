import datetime

from django.db import models
from django.utils import timezone
from .admin import User


class Comment(models.Model):
    """
    Comments are made by users on Posts and other Comments. They are recursive by nature
    we restrict a max depth of 3.

    Note:
    A ForeignObject, is a more flexible way of defining a foreign key relationship.
    It allows you to customize the way the foreign key relationship is handled.
    For example, you can use a ForeignObject to define a relationship where the
    foreign key is not on the primary key of the target model.
    You can also use it to define a relationship with a non-integer primary key.
    """

    # ...
    def __str__(self):
        return f"{self.author_name} - {self.title}"

    title = models.CharField(max_length=240)
    content = models.CharField(max_length=500)
    author_name = models.CharField(max_length=50)


class Tag(models.Model):
    """
    A tag is a keyword associated with another model of the forum application.
    """
    def __str__(self):
        return f"{self.name}"

    name = models.CharField(max_length=50)


class Topic(models.Model):
    """
    A topic represents a "channel" of related posts within an arbitrarily configured category.
    """
    def __str__(self):
        return f"{self.title} {self.sub_title}"

    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)


class Post(models.Model):
    created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, blank=True, default='')
    content = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.user.name} - {self.title}"

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateTimeField()
    notify = models.BooleanField()

    def __str__(self):
        return f"{self.user.name} - {self.title}"


