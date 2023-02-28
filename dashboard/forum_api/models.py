import datetime
from uuid import uuid4

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Default fields
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Custom Fields
    company = models.CharField(max_length=100)
    username = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'location', 'country']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                name="unique_username",
            ),
        ]

    def __str__(self):
        return f"{self.username}"

    def get_by_username(self, username):
        return self.get(username=username)


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


